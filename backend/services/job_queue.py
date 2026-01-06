import asyncio
import sqlite3
from typing import Optional, List
import json
from datetime import datetime, timedelta
from backend.core.config import settings


class JobQueue:
    def __init__(self):
        self.db_path = settings.database_url.replace("sqlite+aiosqlite:///", "")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                status TEXT NOT NULL,
                progress INTEGER DEFAULT 0,
                current_step TEXT,
                input TEXT NOT NULL,
                result TEXT,
                error TEXT,
                started_at TIMESTAMP,
                updated_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    async def create_job(self, job_type: str, input_data: dict) -> str:
        import uuid
        job_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO jobs (id, type, status, input, started_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (job_id, job_type, "pending", json.dumps(input_data), now, now))
        conn.commit()
        conn.close()

        return job_id

    async def update_job(self, job_id: str, **kwargs):
        allowed_fields = {"status", "progress", "current_step", "result", "error", "completed_at"}

        updates = []
        values = []
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                if field == "result":
                    values.append(json.dumps(value) if value is not None else None)
                elif field in ["progress"]:
                    values.append(int(value))
                else:
                    values.append(value)

        if not updates:
            return

        values.append(datetime.utcnow().isoformat())
        values.append(job_id)

        query = f"UPDATE jobs SET {', '.join(updates)}, updated_at = ? WHERE id = ?"

        conn = sqlite3.connect(self.db_path)
        conn.execute(query, values)
        conn.commit()
        conn.close()

    async def get_job(self, job_id: str) -> Optional[dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return self._row_to_dict(row)

    async def list_jobs(self, status: Optional[str] = None, limit: int = 10) -> List[dict]:
        conn = sqlite3.connect(self.db_path)
        if status:
            cursor = conn.execute(
                "SELECT * FROM jobs WHERE status = ? ORDER BY started_at DESC LIMIT ?",
                (status, limit)
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM jobs ORDER BY started_at DESC LIMIT ?",
                (limit,)
            )
        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    async def cancel_job(self, job_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "UPDATE jobs SET status = ?, completed_at = ?, updated_at = ? WHERE id = ? AND status IN (?, ?)",
            ("cancelled", datetime.utcnow().isoformat(), datetime.utcnow().isoformat(), job_id, "pending", "running")
        )
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        return rows_affected > 0

    async def cleanup_old_jobs(self, days: int = 30):
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM jobs WHERE started_at < ? AND status = 'completed'", (cutoff,))
        conn.commit()
        conn.close()

    def _row_to_dict(self, row) -> dict:
        return {
            "id": row[0],
            "type": row[1],
            "status": row[2],
            "progress": row[3],
            "current_step": row[4],
            "input": json.loads(row[5]),
            "result": json.loads(row[6]) if row[6] else None,
            "error": row[7],
            "started_at": row[8],
            "updated_at": row[9],
            "completed_at": row[10]
        }


class JobCancelledException(Exception):
    pass
