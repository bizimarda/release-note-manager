from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class JobType(str, Enum):
    FETCH_JIRA_ISSUES = "fetch_jira_issues"
    FETCH_GITHUB_CHANGES = "fetch_github_changes"
    AI_ANALYZE_CHANGES = "ai_analyze_changes"
    GENERATE_RELEASE_NOTES = "generate_release_notes"
    GENERATE_ALL = "generate_all"


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class GenerateRequest(BaseModel):
    jira_input: str = Field(..., description="Jira task number or JQL filter")
    input_type: str = Field("task", description="Type: 'task' or 'jql'")
    version: Optional[str] = Field(None, description="Version number or auto-detect")
    release_date: Optional[str] = Field(None, description="Release date (DD/MM/YYYY)")
    author: Optional[str] = Field(None, description="Release author")
    release_name: Optional[str] = Field(None, description="Release name")


class JobResponse(BaseModel):
    id: str
    type: str
    status: str
    progress: int
    current_step: Optional[str] = None
    input: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    updated_at: Optional[str] = None
    completed_at: Optional[str] = None


class ReleaseNoteSection(BaseModel):
    title: str
    content: str


class ReleaseNote(BaseModel):
    id: str
    job_id: str
    service_name: str
    version: str
    release_date: str
    author: Optional[str] = None
    release_name: Optional[str] = None
    content: str
    jira_tasks: Optional[List[Dict[str, Any]]] = None
    created_at: str
    updated_at: str


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: Optional[List[str]] = None
    code: Optional[str] = None


class SuccessResponse(BaseModel):
    success: bool = True
    data: Any
    message: str = "Success"
