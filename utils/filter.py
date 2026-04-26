from typing import Dict, Any
from config.config import config

def keyword_filter(job: Dict[str, Any]) -> bool:
    """
    Filters a job based on configured inclusion and exclusion keywords.
    
    Args:
        job (Dict[str, Any]): The job dictionary containing 'title' and 'description'.
        
    Returns:
        bool: True if the job passes the filter, False otherwise.
    """
    preferences = config.PREFERENCES
    if not preferences:
        return True
        
    keywords_config = preferences.get("keywords", {})
    includes = [k.lower() for k in keywords_config.get("include", [])]
    excludes = [k.lower() for k in keywords_config.get("exclude", [])]
    
    text_to_search = (job.get("title", "") + " " + job.get("description", "")).lower()
    
    # Check exclusions first
    for exclude in excludes:
        if exclude in text_to_search:
            return False
            
    # Check inclusions
    if includes:
        has_include = any(include in text_to_search for include in includes)
        if not has_include:
            return False
            
    return True
