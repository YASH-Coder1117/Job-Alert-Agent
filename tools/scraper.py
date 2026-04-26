import time
import math
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from utils.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

def clean_html_with_beautifulsoup(html_text: str) -> str:
    """
    Uses BeautifulSoup to strip messy HTML tags and return clean text
    for our MegaLLM evaluator.
    """
    if not html_text or not isinstance(html_text, str):
        return ""
    
    soup = BeautifulSoup(html_text, "html.parser")
    # Extract text with spaces between tags
    clean_text = soup.get_text(separator=' ', strip=True)
    return clean_text

def scrape_jobs_universal(query: str, location: str) -> List[Dict[str, Any]]:
    """
    Uses JobSpy to scrape multiple portals (LinkedIn, Indeed, Glassdoor) simultaneously.
    Returns a normalized list of job dictionaries.
    """
    logger.info(f"Starting JobSpy scraping for query: '{query}' at '{location}' on LinkedIn, Indeed, and Glassdoor")
    
    try:
        from jobspy import scrape_jobs
        
        # We search across multiple portals
        jobs_df = scrape_jobs(
            site_name=["indeed", "linkedin", "glassdoor"],
            search_term=query,
            location=location,
            results_wanted=15, # Total results requested
            country_america=False # Allows international searches
        )
        
        if jobs_df.empty:
            logger.warning("JobSpy returned an empty dataframe. (Potentially blocked or no results).")
            raise Exception("Empty DataFrame")
            
        jobs = []
        # JobSpy returns a pandas DataFrame. We convert it to records.
        records = jobs_df.to_dict('records')
        
        for record in records:
            # Clean the description using BeautifulSoup
            raw_description = record.get('description', '')
            clean_desc = clean_html_with_beautifulsoup(raw_description)
            
            # JobSpy uses slightly different column names, we map them to our schema
            title = record.get('title', 'Unknown Title')
            
            # Handle pandas NaNs
            if pd.isna(title):
                continue
                
            company = record.get('company', 'Unknown Company')
            loc = record.get('location', location)
            job_url = record.get('job_url', '')
            
            # Pandas NaN check
            company = str(company) if not pd.isna(company) else "Unknown Company"
            loc = str(loc) if not pd.isna(loc) else "Unknown Location"
            job_url = str(job_url) if not pd.isna(job_url) else ""
            
            jobs.append({
                "title": str(title),
                "company": company,
                "location": loc,
                "link": job_url,
                "description": clean_desc
            })
            
        logger.info(f"Successfully scraped {len(jobs)} jobs across multiple portals.")
        return jobs
        
    except Exception as e:
        logger.error(f"Error during JobSpy scraping: {e}")
        logger.info("Generating fallback mock jobs so the pipeline can still be tested...")
        
        run_id = int(time.time())
        # Fallback mock data to ensure the rest of the pipeline (Vector DB, LLM, Email) can be tested
        
        raw_mock_html = f"<p>We are looking for an experienced <strong>{query}</strong> with deep knowledge of Python, Machine Learning, and NLP.</p><ul><li>Lead AI initiatives</li></ul>"
        clean_mock_desc = clean_html_with_beautifulsoup(raw_mock_html)
        
        jobs = [
            {
                "title": f"Senior {query} (Mock ID: {run_id})",
                "company": "Tech Innovations Inc.",
                "location": location,
                "link": f"https://www.indeed.com/viewjob?jk=senior_mock_{run_id}",
                "description": clean_mock_desc
            },
            {
                "title": f"Junior {query} (Mock ID: {run_id})",
                "company": "StartupAI",
                "location": location,
                "link": f"https://www.indeed.com/viewjob?jk=junior_mock_{run_id}",
                "description": "Looking for a passionate fresher to join our team. Experience in Python and deep learning basics required."
            },
            {
                "title": f"Data Scientist (Mock ID: {run_id})",
                "company": "Global Corp",
                "location": location,
                "link": f"https://www.indeed.com/viewjob?jk=ds_mock_{run_id}",
                "description": "General data science role. Needs Python and basic ML skills."
            }
        ]
        return jobs
