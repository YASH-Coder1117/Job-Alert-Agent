from typing import Dict, Any
from tools.llm_client import generate_completion
from utils.logger import get_logger

logger = get_logger(__name__)

def is_relevant(job: Dict[str, Any], preferences: Dict[str, Any]) -> bool:
    """
    Evaluates if a job is relevant based on user preferences using the MegaLLM local model.
    
    Args:
        job (Dict[str, Any]): The job dictionary containing title and description.
        preferences (Dict[str, Any]): The user preferences dict.
        
    Returns:
        bool: True if the model deems it relevant, False otherwise.
    """
    prompt = f"""
    Evaluate if this job is highly relevant to the user preferences.

    User preferences:
    Role: {preferences.get('role', 'N/A')}
    Experience level: {preferences.get('experience', 'N/A')}
    Skills desired: {', '.join(preferences.get('skills', []))}
    Location: {preferences.get('location', 'N/A')}

    Job Listing:
    Title: {job.get('title', 'N/A')}
    Company: {job.get('company', 'N/A')}
    Location: {job.get('location', 'N/A')}
    Description: {job.get('description', 'N/A')}

    Are the user's skills and experience a good match for this job? 
    Answer YES or NO only. Do not provide any explanation.
    """
    
    logger.debug(f"Evaluating job: {job.get('title')} at {job.get('company')}")
    
    response = generate_completion(prompt)
    
    result = "YES" in response.upper()
    logger.info(f"Evaluation result for {job.get('title')}: {'Relevant' if result else 'Not Relevant'}")
    
    return result
