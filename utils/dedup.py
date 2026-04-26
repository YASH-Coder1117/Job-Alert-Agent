import hashlib
from typing import Dict, Any

def generate_hash(job: Dict[str, Any]) -> str:
    """
    Generate a unique MD5 hash for a job based on its title, company, and location.
    
    Args:
        job (Dict[str, Any]): A dictionary containing 'title', 'company', and 'location'.
        
    Returns:
        str: An MD5 hash string representing the unique job.
    """
    title = job.get('title', '').strip().lower()
    company = job.get('company', '').strip().lower()
    location = job.get('location', '').strip().lower()
    
    unique_string = f"{title}_{company}_{location}"
    return hashlib.md5(unique_string.encode('utf-8')).hexdigest()
