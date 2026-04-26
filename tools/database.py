import psycopg2
from typing import List, Dict, Any
from config.config import config
from utils.logger import get_logger

logger = get_logger(__name__)

def get_connection():
    """Returns a connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(
            host=config.DB_HOST,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

def initialize_db():
    """Initializes the database schema including the pgvector extension."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    job_hash TEXT UNIQUE NOT NULL,
                    title TEXT,
                    company TEXT,
                    location TEXT,
                    link TEXT,
                    description TEXT,
                    notified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    embedding vector(384)
                );
            """)
            # For small test datasets, ivfflat with lists=100 causes 0 results because of empty probes.
            # It's better to use exact search (no index) or hnsw. We'll drop the ivfflat index to ensure results are found.
            try:
                cur.execute("DROP INDEX IF EXISTS idx_jobs_embedding;")
            except Exception:
                pass
            conn.commit()
            
            # Safe migrations using individual transactions
            try:
                with conn.cursor() as mig_cur:
                    mig_cur.execute("ALTER TABLE jobs ADD COLUMN IF NOT EXISTS link TEXT;")
                conn.commit()
            except Exception:
                conn.rollback()
            logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        conn.rollback()
    finally:
        conn.close()

def insert_job(job: Dict[str, Any]):
    """Inserts a job into the database with its embedding."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO jobs (job_hash, title, company, location, link, description, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (job_hash) DO NOTHING;
            """, (
                job.get('hash'), 
                job.get('title'), 
                job.get('company'), 
                job.get('location'), 
                job.get('link', ''),
                job.get('description'), 
                job.get('embedding')
            ))
            conn.commit()
            logger.debug(f"Inserted job {job.get('hash')} into DB.")
    except Exception as e:
        logger.error(f"Failed to insert job: {e}")
        conn.rollback()
    finally:
        conn.close()

def job_exists(job_hash: str) -> bool:
    """Checks if a job already exists in the database by its hash."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM jobs WHERE job_hash = %s;", (job_hash,))
            return cur.fetchone() is not None
    except Exception as e:
        logger.error(f"Failed to check job existence: {e}")
        return False
    finally:
        conn.close()

def search_similar_jobs(query_embedding: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
    """Searches for similar jobs using pgvector's cosine distance."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT title, company, location, link, description
                FROM jobs
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
            """, (query_embedding, top_k))
            
            results = cur.fetchall()
            return [
                {
                    "title": r[0],
                    "company": r[1],
                    "location": r[2],
                    "link": r[3],
                    "description": r[4]
                }
                for r in results
            ]
    except Exception as e:
        logger.error(f"Failed to search similar jobs: {e}")
        return []
    finally:
        conn.close()
