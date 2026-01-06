from fastapi import APIRouter
from backend.models.schemas import SuccessResponse
from backend.services.github_service import GitHubClient
from backend.core.config import settings

router = APIRouter(prefix="/api/github", tags=["github"])


@router.get("/repositories", response_model=SuccessResponse)
async def list_repositories():
    """List all repositories in the configured GitHub organization"""
    github = GitHubClient()

    try:
        repos = await github.list_org_repositories(settings.github_org)

        return {
            "success": True,
            "data": {
                "organization": settings.github_org,
                "count": len(repos),
                "repositories": [
                    {
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "description": repo.get("description", ""),
                        "language": repo.get("language", ""),
                        "updated_at": repo["updated_at"],
                        "stars": repo.get("stargazers_count", 0),
                        "url": repo["html_url"]
                    }
                    for repo in repos
                ]
            },
            "message": f"Found {len(repos)} repositories"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "message": f"Failed to list repositories: {str(e)}"
        }
