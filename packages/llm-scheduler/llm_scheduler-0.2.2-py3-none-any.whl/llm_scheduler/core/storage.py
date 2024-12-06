from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
import json
import sqlite3
from datetime import datetime
import os
from supabase import Client, create_client

class BaseStorage(ABC):
    """Abstract base class for storage backends"""
    
    @abstractmethod
    async def store_job(self, job_data: dict) -> None:
        pass

    @abstractmethod
    async def get_job(self, job_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def update_job_status(self, job_id: str, status: str) -> None:
        pass

class SupabaseStorage(BaseStorage):
    """Supabase storage implementation"""
    
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)
    
    async def store_job(self, job_data: dict) -> None:
        self.client.table('scheduled_jobs').insert(job_data).execute()
    
    async def get_job(self, job_id: str) -> Optional[dict]:
        response = self.client.table('scheduled_jobs')\
            .select('*')\
            .eq('job_id', job_id)\
            .single()\
            .execute()
        return response.data if response.data else None
    
    async def update_job_status(self, job_id: str, status: str) -> None:
        self.client.table('scheduled_jobs')\
            .update({'status': status})\
            .eq('job_id', job_id)\
            .execute()

class SQLiteStorage(BaseStorage):
    """SQLite storage implementation"""
    
    def __init__(self, db_path: str = "scheduler.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create jobs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_jobs (
                job_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                run_date TEXT NOT NULL,
                metadata TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT,
                last_run TEXT,
                next_run TEXT,
                retry_count INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()

    async def store_job(self, job_data: dict) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO scheduled_jobs 
            (job_id, status, run_date, metadata, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            job_data["job_id"],
            job_data["status"],
            job_data["run_date"],
            json.dumps(job_data["metadata"]),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()

    async def get_job(self, job_id: str) -> Optional[dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM scheduled_jobs WHERE job_id = ?",
            (job_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "job_id": row[0],
                "status": row[1],
                "run_date": row[2],
                "metadata": json.loads(row[3]),
                "created_at": row[4],
                "updated_at": row[5],
                "last_run": row[6],
                "next_run": row[7],
                "retry_count": row[8]
            }
        return None

    async def update_job_status(self, job_id: str, status: str) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE scheduled_jobs 
            SET status = ?, updated_at = ?
            WHERE job_id = ?
        """, (status, datetime.now().isoformat(), job_id))
        
        conn.commit()
        conn.close() 

def get_storage(storage_type: str = "sqlite", **kwargs) -> BaseStorage:
    """Factory function to get storage backend"""
    if storage_type == "supabase":
        url = kwargs.get("url") or os.getenv("SUPABASE_URL")
        key = kwargs.get("key") or os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            raise ValueError("Supabase URL and key are required")
        return SupabaseStorage(url, key)
    elif storage_type == "sqlite":
        return SQLiteStorage(kwargs.get("db_path", "scheduler.db"))
    else:
        raise ValueError(f"Unknown storage type: {storage_type}")