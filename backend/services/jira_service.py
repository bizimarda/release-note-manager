import httpx
from typing import List, Dict, Any, Optional
from backend.core.config import settings
import base64


def _parse_atlassian_doc(doc: Any) -> str:
    if not doc or not isinstance(doc, dict):
        return ""

    if doc.get('type') == 'doc':
        content = doc.get('content', [])
        text_parts = []

        def extract_text(nodes):
            for node in nodes:
                if node.get('type') == 'text':
                    text_parts.append(node.get('text', ''))
                elif node.get('content'):
                    extract_text(node.get('content', []))

        extract_text(content)
        return ''.join(text_parts)

    return ""


class JiraClient:
    def __init__(self):
        self.base_url = settings.jira_url.rstrip("/")
        self.email = settings.jira_email.strip() if settings.jira_email else ""
        self.api_token = settings.jira_api_token.strip() if settings.jira_api_token else ""

        auth_str = f"{self.email}:{self.api_token}"
        auth_bytes = auth_str.encode("utf-8")
        auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")

        self.headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}/rest/api/3/{endpoint}"
            response = await client.request(method, url, headers=self.headers, json=data)
            if not response.is_success:
                raise Exception(f"HTTP error! status: {response.status_code}, Response: {response.text[:200]}")
            return response.json()

    async def get_issue(self, issue_key: str) -> Dict:
        return await self._request("GET", f"issue/{issue_key}")

    async def search_issues(self, jql: str, max_results: int = 100) -> Dict:
        return await self._request("POST", "search/jql", {
            "jql": jql,
            "maxResults": max_results,
            "fields": [
                "summary", "description", "status", "labels", "components",
                "assignee", "reporter", "priority", "issuetype", "project",
                "created", "updated", "resolution",
                "customfield_10049",  # Release Notes
                "customfield_10055",  # Configuration Notes
                "customfield_10074",  # API Change
                "customfield_10077",  # Application Config
                "customfield_10056",  # Is Jenkins pipeline successful?
                "customfield_10100",  # Database Migrations
                "customfield_10101",  # DevOps Changes
                "customfield_10102",  # Known Issues
                "customfield_10103"   # CVEs
            ]
        })

    async def get_issue_fields(self, issue_key: str) -> Dict:
        issue = await self.get_issue(issue_key)
        fields = issue["fields"]

        release_notes_field = fields.get("customfield_10049")
        config_notes_field = fields.get("customfield_10055")
        api_change_field = fields.get("customfield_10074")
        app_config_field = fields.get("customfield_10077")
        jenkins_field = fields.get("customfield_10056")
        db_migration_field = fields.get("customfield_10100")
        devops_field = fields.get("customfield_10101")
        known_issues_field = fields.get("customfield_10102")
        cves_field = fields.get("customfield_10103")

        release_notes = ""
        config_notes = ""
        api_change = ""
        app_config = ""
        jenkins = ""

        if release_notes_field:
            if isinstance(release_notes_field, dict) and 'value' in release_notes_field:
                release_notes = release_notes_field['value']
            elif isinstance(release_notes_field, str):
                release_notes = release_notes_field
            elif isinstance(release_notes_field, dict):
                release_notes = _parse_atlassian_doc(release_notes_field)

        if config_notes_field:
            if isinstance(config_notes_field, dict) and 'value' in config_notes_field:
                config_notes = config_notes_field['value']
            elif isinstance(config_notes_field, str):
                config_notes = config_notes_field
            elif isinstance(config_notes_field, dict):
                config_notes = _parse_atlassian_doc(config_notes_field)

        if api_change_field:
            if isinstance(api_change_field, dict) and 'value' in api_change_field:
                api_change = api_change_field['value']
            elif isinstance(api_change_field, str):
                api_change = api_change_field

        if app_config_field:
            if isinstance(app_config_field, dict) and 'value' in app_config_field:
                app_config = app_config_field['value']
            elif isinstance(app_config_field, str):
                app_config = app_config_field

        if jenkins_field:
            if isinstance(jenkins_field, dict) and 'value' in jenkins_field:
                jenkins = jenkins_field['value']
            elif isinstance(jenkins_field, str):
                jenkins = jenkins_field

        return {
            "key": issue["key"],
            "summary": fields["summary"],
            "description": _parse_atlassian_doc(fields.get("description")),
            "status": fields["status"]["name"],
            "labels": fields.get("labels", []),
            "components": [c["name"] for c in fields.get("components", [])],
            "assignee": fields["assignee"]["displayName"] if fields.get("assignee") else None,
            "reporter": fields["reporter"]["displayName"] if fields.get("reporter") else None,
            "priority": fields["priority"]["name"] if fields.get("priority") else None,
            "issue_type": fields["issuetype"]["name"],
            "project": fields["project"]["key"],
            "project_name": fields["project"]["name"],
            "created": fields["created"],
            "updated": fields["updated"],
            "release_notes": release_notes,
            "configuration_notes": config_notes,
            "api_change": api_change,
            "app_config": app_config,
            "jenkins_successful": jenkins,
            "database_migration": db_migration_field,
            "devops_changes": devops_field,
            "known_issues": known_issues_field,
            "cves": cves_field,
            "all_fields": fields
        }

    async def get_epic_with_stories(self, epic_key: str) -> Dict:
        epic = await self.get_issue_fields(epic_key)
        jql = f"'Epic Link' = {epic_key}"
        stories_result = await self.search_issues(jql)

        stories = []
        for issue in stories_result.get("issues", []):
            story = await self.get_issue_fields(issue["key"])
            stories.append(story)

        return {
            "epic": epic,
            "stories": stories
        }

    async def get_issues_by_keys(self, keys: List[str]) -> List[Dict]:
        jql = f"key in ({', '.join(keys)})"
        result = await self.search_issues(jql, max_results=len(keys))
        issues = []
        for issue in result.get("issues", []):
            issues.append(await self.get_issue_fields(issue["key"]))
        return issues

    async def get_project_components(self, project_key: str) -> List[Dict]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}/rest/api/3/project/{project_key}/components"
            response = await client.get(url, headers=self.headers)

            if not response.is_success:
                raise Exception(f"HTTP error! status: {response.status_code}, Response: {response.text[:200]}")

            return response.json()
