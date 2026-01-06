import httpx
from typing import List, Dict, Any, Optional
from backend.core.config import settings


class GitHubClient:
    def __init__(self):
        self.base_url = settings.github_api_url
        self.token = settings.github_token.strip() if settings.github_token else ""
        import logging
        logging.getLogger(__name__).info(f"GitHub token loaded: {'YES' if self.token else 'NO'}")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}/{endpoint}"
            response = await client.request(method, url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()

    async def get_branches(self, owner: str, repo: str) -> List[Dict]:
        return await self._request("GET", f"repos/{owner}/{repo}/branches")

    async def get_commits(self, owner: str, repo: str, branch: str = None) -> List[Dict]:
        endpoint = f"repos/{owner}/{repo}/commits"
        if branch:
            endpoint += f"?sha={branch}"
        return await self._request("GET", endpoint)

    async def get_commit(self, owner: str, repo: str, sha: str) -> Dict:
        return await self._request("GET", f"repos/{owner}/{repo}/commits/{sha}")

    async def get_diff(self, owner: str, repo: str, sha: str) -> str:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}/repos/{owner}/{repo}/commits/{sha}"
            response = await client.get(url, headers=self.headers, params={"media_type": "diff"})
            response.raise_for_status()
            return response.text

    async def get_file_content(self, owner: str, repo: str, path: str, ref: str = "main") -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
                response = await client.get(url, headers=self.headers, params={"ref": ref})
                response.raise_for_status()
                data = response.json()
                if data.get("encoding") == "base64":
                    import base64
                    content = base64.b64decode(data["content"]).decode("utf-8")
                    return content
        except Exception:
            return None

    async def get_tags(self, owner: str, repo: str) -> List[Dict]:
        return await self._request("GET", f"repos/{owner}/{repo}/tags")

    async def find_branches_by_task(self, owner: str, repo: str, task_number: str) -> List[Dict]:
        branches = await self.get_branches(owner, repo)
        matching_branches = []

        for branch in branches:
            if task_number in branch["name"]:
                commits = await self.get_commits(owner, repo, branch["name"])
                if commits:
                    matching_branches.append({
                        "name": branch["name"],
                        "sha": branch["commit"]["sha"],
                        "last_commit": commits[0]
                    })

        return matching_branches

    async def get_repository_info(self, owner: str, repo: str) -> Dict:
        return await self._request("GET", f"repos/{owner}/{repo}")

    async def list_org_repositories(self, org: str) -> List[Dict]:
        endpoint = f"orgs/{org}/repos?sort=updated&per_page=100"
        return await self._request("GET", endpoint)

    def parse_git_tag_version(self, tag_name: str) -> Optional[str]:
        import re
        match = re.match(r'v?(\d+\.\d+\.\d+)', tag_name)
        if match:
            return match.group(1)
        return None

    async def get_pull_requests(self, owner: str, repo: str, state: str = "all") -> List[Dict]:
        endpoint = f"repos/{owner}/{repo}/pulls?state={state}&per_page=100"
        return await self._request("GET", endpoint)

    async def get_pull_request(self, owner: str, repo: str, pr_number: int) -> Dict:
        return await self._request("GET", f"repos/{owner}/{repo}/pulls/{pr_number}")

    async def get_pull_request_commits(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        return await self._request("GET", f"repos/{owner}/{repo}/pulls/{pr_number}/commits")

    async def get_pull_request_files(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        return await self._request("GET", f"repos/{owner}/{repo}/pulls/{pr_number}/files")

    async def get_pull_request_comments(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        endpoint = f"repos/{owner}/{repo}/pulls/{pr_number}/comments"
        return await self._request("GET", endpoint)

    async def get_pull_request_reviews(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        return await self._request("GET", f"repos/{owner}/{repo}/pulls/{pr_number}/reviews")

    async def find_pull_requests_by_task(self, owner: str, repo: str, task_number: str) -> List[Dict]:
        all_prs = await self.get_pull_requests(owner, repo)
        matching_prs = []

        for pr in all_prs:
            pr_title = pr.get("title", "")
            pr_head = pr.get("head", {}).get("ref", "")
            pr_body = pr.get("body", "")

            if task_number in pr_title or task_number in pr_head:
                pr_commits = await self.get_pull_request_commits(owner, repo, pr["number"])
                pr_comments = await self.get_pull_request_comments(owner, repo, pr["number"])
                pr_reviews = await self.get_pull_request_reviews(owner, repo, pr["number"])

                matching_prs.append({
                    "number": pr["number"],
                    "title": pr["title"],
                    "state": pr["state"],
                    "merged": pr.get("merged", False),
                    "merged_at": pr.get("merged_at"),
                    "head_branch": pr.get("head", {}).get("ref", ""),
                    "base_branch": pr.get("base", {}).get("ref", ""),
                    "body": pr_body,
                    "commits": pr_commits,
                    "comments": pr_comments,
                    "reviews": pr_reviews,
                    "url": pr["html_url"]
                })

        return matching_prs
