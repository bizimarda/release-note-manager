import asyncio
import logging
from datetime import datetime
from typing import Optional
from backend.services.job_queue import JobQueue, JobCancelledException
from backend.services.jira_service import JiraClient
from backend.services.github_service import GitHubClient
from backend.services.ai_service import AIService
from backend.services.release_notes_generator import ReleaseNotesGenerator
from backend.core.config import settings

logger = logging.getLogger(__name__)


class JobWorker:
    def __init__(self, job_queue: JobQueue):
        self.queue = job_queue
        self.jira = JiraClient()
        self.github = GitHubClient()
        self.ai = AIService()
        self.generator = ReleaseNotesGenerator()
        self.running = False
        self.cancelled_jobs = set()

    async def start(self):
        self.running = True
        logger.info("Job worker started")

        while self.running:
            job = await self._get_next_pending_job()
            if job:
                await self._process_job(job)
            else:
                await asyncio.sleep(1)

    async def _get_next_pending_job(self) -> Optional[dict]:
        jobs = await self.queue.list_jobs(status="pending", limit=1)
        return jobs[0] if jobs else None

    async def _process_job(self, job: dict):
        job_id = job["id"]

        try:
            await self.queue.update_job(job_id, status="running", current_step="Starting...", progress=0)

            await self._check_cancelled(job_id)

            if job["type"] == "generate_all":
                await self._generate_all(job)
            else:
                raise ValueError(f"Unknown job type: {job['type']}")

            await self.queue.update_job(job_id, status="completed", progress=100, current_step="Completed")

        except JobCancelledException:
            await self.queue.update_job(job_id, status="cancelled", current_step="Cancelled by user")
            self.cancelled_jobs.discard(job_id)
            logger.info(f"Job {job_id} cancelled")

        except Exception as e:
            await self.queue.update_job(
                job_id,
                status="failed",
                current_step=f"Failed: {str(e)}",
                error=str(e)
            )
            logger.error(f"Job {job_id} failed: {e}", exc_info=True)

    async def cancel_job(self, job_id: str):
        self.cancelled_jobs.add(job_id)
        success = await self.queue.cancel_job(job_id)
        return success

    async def _generate_all(self, job: dict):
        job_id = job["id"]
        input_data = job["input"]

        await self.queue.update_job(job_id, current_step="Fetching Jira tasks...", progress=5)
        await self._check_cancelled(job_id)

        jira_tasks = await self._fetch_jira_tasks(input_data)

        await self.queue.update_job(job_id, current_step="Mapping to GitHub repositories...", progress=10)
        await self._check_cancelled(job_id)

        github_mappings = await self._map_to_github(jira_tasks)

        await self.queue.update_job(job_id, current_step="Fetching GitHub changes...", progress=20)
        await self._check_cancelled(job_id)

        github_changes = await self._fetch_github_changes(github_mappings)

        await self.queue.update_job(job_id, current_step="AI analyzing changes...", progress=30)
        await self._check_cancelled(job_id)

        analyses = await self._analyze_changes(github_changes, jira_tasks)

        await self.queue.update_job(job_id, current_step="Generating release notes...", progress=80)
        await self._check_cancelled(job_id)

        try:
            release_notes = await self._generate_service_release_notes(analyses, jira_tasks, input_data)
            logger.info(f"Generated {len(release_notes)} service release notes: {list(release_notes.keys())}")
        except Exception as e:
            logger.error(f"Failed to generate release notes: {e}", exc_info=True)
            release_notes = {}

        if not release_notes:
            await self.queue.update_job(
                job_id,
                result={},
                current_step="No release notes generated",
                progress=90
            )
        else:
            await self.queue.update_job(job_id, result=release_notes, current_step="Saving results...", progress=90)

    async def _fetch_jira_tasks(self, input_data: dict) -> list:
        jira_input = input_data.get("jira_input", "")
        input_type = input_data.get("input_type", "task")

        if input_type == "task":
            tasks_input = [t.strip() for t in jira_input.split(",") if t.strip()]
            
            if len(tasks_input) == 1:
                issue = await self.jira.get_issue_fields(tasks_input[0])

                if issue.get("issue_type") == "Epic":
                    result = await self.jira.get_epic_with_stories(tasks_input[0])
                    return [result["epic"]] + result["stories"]
                else:
                    return [issue]
            else:
                return await self.jira.get_issues_by_keys(tasks_input)
        elif input_type == "jql":
            result = await self.jira.search_issues(jira_input)
            tasks = []
            for issue in result.get("issues", []):
                tasks.append(await self.jira.get_issue_fields(issue["key"]))
            return tasks
        else:
            raise Exception(f"Unsupported input_type: {input_type}")

    async def _map_to_github(self, jira_tasks: list) -> list:
        from backend.core.config import settings
        import os

        # Load repository mapping from config file
        repo_mapping = {}
        mapping_file = "repo_mapping.conf"

        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            jira_comp, github_repo = line.split('=', 1)
                            repo_mapping[jira_comp.strip().lower()] = github_repo.strip().lower()
            except Exception as e:
                print(f"Warning: Failed to load repo mapping: {e}")

        mappings = []

        for task in jira_tasks:
            components = task.get("components", [])

            if components:
                logger.info(f"Task {task['key']} has components: {components}")
                repo_name = None
                
                # Try all components until a match is found
                for component in components:
                    # Try both formats: with spaces and with dashes
                    component_variants = [
                        component.lower().replace("_", "-").replace(" ", "-"),  # dash-separated
                        component.lower().replace("_", " "),  # space-separated
                        component.lower()  # original lowercase
                    ]
                    
                    for jira_component in component_variants:
                        logger.info(f"  Trying component: '{component}' -> variant: '{jira_component}'")

                        # 1. Check mapping file first
                        repo_name = repo_mapping.get(jira_component)
                        logger.info(f"  Mapping check: '{jira_component}' -> '{repo_name}'")

                        # If we found a match, break the variant loop
                        if repo_name:
                            logger.info(f"  Match found in mapping: '{repo_name}'")
                            break

                    # If we found a match, break the component loop
                    if repo_name:
                        break

                # If no match found in mapping, try the first component with matching
                if not repo_name and components:
                    jira_component = components[0].lower().replace("_", "-").replace(" ", "-")
                    
                    # 2. Try direct match
                    repo_name = jira_component

                    # 3. Try partial matching with available repos
                    from backend.services.github_service import GitHubClient
                    try:
                        github = GitHubClient()
                        repos = await github.list_org_repositories(settings.github_org)
                        repo_names = [repo["name"].lower() for repo in repos]

                        for repo in repo_names:
                            if jira_component in repo or repo in jira_component:
                                repo_name = repo
                                logger.info(f"  Partial match found: '{jira_component}' -> '{repo_name}'")
                                break
                    except Exception as e:
                        print(f"Warning: Failed to fetch repositories for matching: {e}")

                logger.info(f"Task {task['key']} final repo: '{repo_name}'")
                owner = settings.github_org

                mappings.append({
                    "task_key": task["key"],
                    "owner": owner,
                    "repo": repo_name
                })

        return mappings

    async def _fetch_github_changes(self, mappings: list) -> dict:
        changes_by_repo = {}

        for mapping in mappings:
            task_number = mapping["task_key"].split("-")[-1]
            task_key = mapping["task_key"]

            repo_key = f"{mapping['owner']}/{mapping['repo']}"

            if repo_key not in changes_by_repo:
                changes_by_repo[repo_key] = []

            # Scenario 1 & 2: Branch varsa veya PR varsa
            branches = await self.github.find_branches_by_task(
                mapping["owner"],
                mapping["repo"],
                task_number
            )

            prs = await self.github.find_pull_requests_by_task(
                mapping["owner"],
                mapping["repo"],
                task_number
            )

            # PR varsa (open veya merged)
            if prs:
                for pr in prs:
                    # PR commitlerini al
                    pr_commits = pr.get("commits", [])

                    for commit in pr_commits:
                        try:
                            diff = await self.github.get_diff(
                                mapping["owner"],
                                mapping["repo"],
                                commit["sha"]
                            )
                        except Exception as e:
                            logger.warning(f"Failed to get diff for commit {commit.get('sha', 'unknown')}: {e}")
                            diff = ""

                        # PR mesajlarını topla
                        pr_messages = []
                        if pr.get("title"):
                            pr_messages.append(f"PR Title: {pr['title']}")
                        if pr.get("body"):
                            pr_messages.append(f"PR Description: {pr['body']}")

                        # PR yorumlarını topla
                        pr_comments = pr.get("comments", [])
                        if pr_comments:
                            for comment in pr_comments:
                                if comment.get("body"):
                                    pr_messages.append(f"PR Comment: {comment['body']}")

                        # PR review'larını topla
                        pr_reviews = pr.get("reviews", [])
                        if pr_reviews:
                            for review in pr_reviews:
                                if review.get("body"):
                                    pr_messages.append(f"Review Comment: {review['body']}")

                        changes_by_repo[repo_key].append({
                            "branch": pr.get("head_branch", ""),
                            "commit": commit,
                            "diff": diff,
                            "pr_number": pr.get("number"),
                            "pr_title": pr.get("title", ""),
                            "pr_body": pr.get("body", ""),
                            "pr_state": pr.get("state", ""),
                            "pr_merged": pr.get("merged", False),
                            "pr_merged_at": pr.get("merged_at"),
                            "pr_messages": pr_messages,
                            "pr_comments": pr_comments,
                            "pr_reviews": pr_reviews,
                            "pr_url": pr.get("url", ""),
                            "task_key": task_key
                        })

            # Sadece branch varsa (PR yok)
            elif branches:
                for branch in branches:
                    commits = await self.github.get_commits(
                        mapping["owner"],
                        mapping["repo"],
                        branch["name"]
                    )

                    for commit in commits:
                        try:
                            diff = await self.github.get_diff(
                                mapping["owner"],
                                mapping["repo"],
                                commit["sha"]
                            )
                        except Exception as e:
                            logger.warning(f"Failed to get diff for commit {commit.get('sha', 'unknown')}: {e}")
                            diff = ""

                        changes_by_repo[repo_key].append({
                            "branch": branch["name"],
                            "commit": commit,
                            "diff": diff,
                            "task_key": task_key
                        })

            # Scenario 3: Branch yok ama merge edilmiş PR olabilir - daha önce kontrol edildi
            # Eğer hiç değişiklik bulunamazsa log at
            if not changes_by_repo.get(repo_key):
                logger.info(f"No branches or PRs found for task {task_key} in {repo_key}")

        return changes_by_repo

    async def _analyze_changes(self, github_changes: dict, jira_tasks: list) -> dict:
        analyses_by_repo = {}

        for repo_key, changes in github_changes.items():
            analyses = []

            for change in changes:
                task_key = change.get("task_key") or next(
                    (t["key"] for t in jira_tasks if t["key"].split("-")[-1] in change["branch"]),
                    None
                )

                jira_context = next((t for t in jira_tasks if t["key"] == task_key), {})

                if task_key:
                    # PR context'i hazırla
                    pr_context = {
                        "pr_number": change.get("pr_number"),
                        "pr_title": change.get("pr_title"),
                        "pr_body": change.get("pr_body"),
                        "pr_state": change.get("pr_state"),
                        "pr_merged": change.get("pr_merged"),
                        "pr_messages": change.get("pr_messages", []),
                        "pr_comments": change.get("pr_comments"),
                        "pr_reviews": change.get("pr_reviews"),
                        "pr_url": change.get("pr_url")
                    }

                    analysis = await self.ai.analyze_code_changes(change["diff"], jira_context, pr_context)
                    analysis["jira_key"] = task_key

                    # PR bilgilerini analize ekle
                    if pr_context.get("pr_number"):
                        analysis["pr_number"] = pr_context["pr_number"]
                        analysis["pr_title"] = pr_context["pr_title"]
                        analysis["pr_url"] = pr_context["pr_url"]
                        analysis["pr_merged"] = pr_context["pr_merged"]

                    # Log the AI analysis result
                    logger.info(f"AI Analysis for {task_key} (PR #{pr_context.get('pr_number', 'N/A')}):")
                    logger.info(f"  Summary: {analysis.get('summary', 'N/A')}")
                    logger.info(f"  Category: {analysis.get('category', 'N/A')}")
                    logger.info(f"  API Changes: {analysis.get('api_changes', [])}")
                    logger.info(f"  Config Changes: {analysis.get('configuration_changes', [])}")
                    logger.info(f"  DB Migrations: {analysis.get('database_migrations', [])}")
                    logger.info(f"  DevOps Changes: {analysis.get('devops_changes', [])}")

                    analyses.append(analysis)

            analyses_by_repo[repo_key] = analyses

        return analyses_by_repo

    def _determine_category_from_jira(self, task: dict) -> str:
        summary = task.get("summary", "").lower()
        issue_type = task.get("issue_type", "").lower()
        release_notes = task.get("release_notes", "").lower()

        keywords = {
            "New Feature": ["implement", "add", "create", "new", "introduce", "feature"],
            "Improvement": ["improve", "enhance", "optimize", "refactor", "update"],
            "Defect Fix": ["fix", "bug", "error", "issue", "problem", "resolve"],
            "Breaking Change": ["breaking", "remove", "deprecate", "remove", "migrate"]
        }

        if issue_type in ["bug", "defect"]:
            return "Defect Fix"

        for category, words in keywords.items():
            for word in words:
                if word in summary or word in release_notes:
                    return category

        return "Improvement"

    async def _generate_service_release_notes(self, analyses: dict, jira_tasks: list, input_data: dict) -> dict:
        logger.info(f"Generating release notes for {len(analyses)} repositories")
        logger.info(f"Available analyses repos: {list(analyses.keys())}")
        logger.info(f"Jira tasks count: {len(jira_tasks)}")

        # Debug: Analyses ve Jira tasks detaylarını logla
        for repo_key, repo_analyses in analyses.items():
            logger.info(f"Repo: {repo_key}, Analyses count: {len(repo_analyses)}")
            for idx, analysis in enumerate(repo_analyses):
                logger.info(f"  Analysis {idx}: summary={analysis.get('summary', 'N/A')[:50]}, category={analysis.get('category', 'N/A')}")

        if not analyses and not jira_tasks:
            logger.warning("No analyses or Jira tasks available, returning empty release notes")
            return {}

        release_notes = {}

        # Eğer analyses varsa, repo bazlı döngü
        if analyses:
            for repo_key, repo_analyses in analyses.items():
                repo_name = repo_key.split("/")[-1]
                service_name = repo_name.replace("-", "_")

                repo_tasks = [t for t in jira_tasks if any(
                    t["key"] == a.get("jira_key")
                    for a in repo_analyses
                )]

                options = {
                    "version": input_data.get("version") or "1.0.0",
                    "release_date": input_data.get("release_date") or datetime.now().strftime("%d/%m/%Y"),
                    "author": input_data.get("author") or "Release Manager",
                    "release_name": input_data.get("release_name") or ""
                }

                # Fallback: Eğer repo_analyses boşsa, tüm jira_tasks'ı kullan
                if not repo_analyses:
                    repo_tasks = jira_tasks
                    logger.warning(f"No analyses for {service_name}, using all {len(jira_tasks)} Jira tasks")

                    # Jira task bilgilerinden empty analysis oluştur
                    effective_analyses = []
                    for task in repo_tasks:
                        category = self._determine_category_from_jira(task)
                        effective_analyses.append({
                            "summary": f"Jira Task {task['key']}: {task.get('summary', '')}",
                            "category": category,
                            "confidence": 0.5,
                            "configuration_changes": [],
                            "database_migrations": [],
                            "devops_changes": [],
                            "cves": [],
                            "api_changes": [],
                            "jira_summary": task.get("summary", ""),
                            "jira_description": task.get("description", ""),
                            "jira_release_notes": task.get("release_notes", ""),
                            "jira_configuration_notes": task.get("configuration_notes", ""),
                            "api_change": task.get("api_change", ""),
                            "app_config": task.get("app_config", ""),
                            "jenkins_successful": task.get("jenkins_successful", ""),
                            "jira_key": task["key"]
                        })
                else:
                    # AI analizlerini kullan, Jira bilgilerini ekle
                    effective_analyses = []
                    for analysis in repo_analyses:
                        # Analysis nesnesini kopyala (dict olarak)
                        analysis_copy = dict(analysis)
                        
                        # İlgili Jira task'ını bul
                        task_key = analysis_copy.get("jira_key")
                        task = next((t for t in jira_tasks if t["key"] == task_key), None)
                        
                        if task:
                            # Jira bilgilerini ekle ama LLM summary'sini koru
                            analysis_copy["jira_summary"] = task.get("summary", "")
                            analysis_copy["jira_description"] = task.get("description", "")
                            analysis_copy["jira_release_notes"] = task.get("release_notes", "")
                            analysis_copy["jira_configuration_notes"] = task.get("configuration_notes", "")
                            analysis_copy["api_change"] = task.get("api_change", "")
                            analysis_copy["app_config"] = task.get("app_config", "")
                            analysis_copy["jenkins_successful"] = task.get("jenkins_successful", "")
                            # Eğer category yoksa, Jira'dan belirle
                            if not analysis_copy.get("category"):
                                analysis_copy["category"] = self._determine_category_from_jira(task)

                            # LLM summary'si yoksa veya boşsa, Jira summary'sini kullan
                            if not analysis_copy.get("summary") or not analysis_copy.get("summary").strip():
                                analysis_copy["summary"] = f"Jira Task {task['key']}: {task.get('summary', '')}"
                                logger.warning(f"Using Jira summary for task {task_key} as LLM summary is empty")
                        
                        effective_analyses.append(analysis_copy)

                content = self.generator.generate_for_service(
                    effective_analyses,
                    repo_tasks,
                    service_name,
                    options
                )

                release_notes[service_name] = {
                    "service_name": service_name,
                    "repo": repo_key,
                    "content": content,
                    "jira_tasks": repo_tasks,
                    **options
                }
        else:
            # Analyses yoksa ama Jira tasks varsa, fallback olarak Jira bilgilerini kullan
            logger.info("No GitHub analyses, using Jira task information only")
            for task in jira_tasks:
                # Task'ten component bilgisini al
                components = task.get("components", [])
                if components:
                    component = components[0].lower().replace("_", "-")
                    service_name = component.replace("-", "_")

                    category = self._determine_category_from_jira(task)

                    # Boş analysis oluştur (fallback)
                    empty_analysis = {
                        "summary": f"Jira Task {task['key']}: {task.get('summary', '')}",
                        "category": category,
                        "confidence": 0.5,
                        "configuration_changes": [],
                        "database_migrations": [],
                        "devops_changes": [],
                        "cves": [],
                        "api_changes": [],
                        "jira_summary": task.get("summary", ""),
                        "jira_description": task.get("description", ""),
                        "jira_release_notes": task.get("release_notes", ""),
                        "jira_configuration_notes": task.get("configuration_notes", ""),
                        "api_change": task.get("api_change", ""),
                        "app_config": task.get("app_config", ""),
                        "jenkins_successful": task.get("jenkins_successful", ""),
                        "jira_key": task["key"]
                    }

                    options = {
                        "version": input_data.get("version") or "1.0.0",
                        "release_date": input_data.get("release_date") or datetime.now().strftime("%d/%m/%Y"),
                        "author": input_data.get("author") or "Release Manager",
                        "release_name": input_data.get("release_name") or ""
                    }

                    content = self.generator.generate_for_service(
                        [empty_analysis],
                        [task],
                        service_name,
                        options
                    )

                    release_notes[service_name] = {
                        "service_name": service_name,
                        "repo": f"{settings.github_org}/{component}",
                        "content": content,
                        "jira_tasks": [task],
                        **options
                    }

        return release_notes

    async def _check_cancelled(self, job_id: str):
        if job_id in self.cancelled_jobs:
            await self.queue.update_job(job_id, status="cancelled", current_step="Cancelled")
            self.cancelled_jobs.discard(job_id)
            raise JobCancelledException("Job was cancelled")

    def stop(self):
        self.running = False
        logger.info("Job worker stopped")
