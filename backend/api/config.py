from fastapi import APIRouter, BackgroundTasks
from backend.models.schemas import SuccessResponse
from backend.services.github_service import GitHubClient
from backend.core.config import settings
import os

router = APIRouter(prefix="/api/config", tags=["config"])


@router.get("/repo-mapping", response_model=SuccessResponse)
async def get_repo_mapping():
    """Get current Jira component → GitHub repository mapping"""
    mapping_file = "repo_mapping.conf"

    if not os.path.exists(mapping_file):
        return {
            "success": True,
            "data": {
                "exists": False,
                "mapping": []
            },
            "message": "No mapping file found"
        }

    mapping = []
    with open(mapping_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                jira_comp, github_repo = line.split('=', 1)
                mapping.append({
                    "jira_component": jira_comp.strip(),
                    "github_repo": github_repo.strip()
                })

    return {
        "success": True,
        "data": {
            "exists": True,
            "mapping": mapping,
            "file_path": mapping_file
        },
        "message": f"Found {len(mapping)} mapping entries"
    }


@router.post("/repo-mapping/sync", response_model=SuccessResponse)
async def sync_repos():
    """Auto-generate mapping by comparing Jira components with GitHub repos"""
    github = GitHubClient()

    try:
        repos = await github.list_org_repositories(settings.github_org)
        repo_names = [repo["name"].lower() for repo in repos]

        suggestions = []

        for repo in repo_names:
            suggestions.append({
                "github_repo": repo,
                "suggested_jira_component": repo.replace("-", "_").replace("_service", "")
            })

        return {
            "success": True,
            "data": {
                "available_repos": repo_names,
                "suggestions": suggestions
            },
            "message": f"Found {len(repo_names)} repositories"
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "message": f"Failed to sync repositories: {str(e)}"
        }
