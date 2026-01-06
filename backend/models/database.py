from sqlalchemy import Column, String, Integer, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    progress = Column(Integer, default=0)
    current_step = Column(String, nullable=True)
    input = Column(Text, nullable=False)
    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class ReleaseNote(Base):
    __tablename__ = "release_notes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    author = Column(String, nullable=True)
    release_name = Column(String, nullable=True)

    content = Column(Text, nullable=False)
    jira_tasks = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Draft(Base):
    __tablename__ = "drafts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
