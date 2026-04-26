from config.config import config
from tools.scraper import scrape_jobs_universal
from tools.embeddings import embed
from tools.database import insert_job, job_exists, search_similar_jobs, initialize_db
from utils.dedup import generate_hash
from utils.filter import keyword_filter
from agents.evaluator import is_relevant
from tools.notifier import send_email
from utils.logger import get_logger

logger = get_logger(__name__)

def run_pipeline():
    """
    Orchestrates the entire job alert pipeline:
    1. Scrapes job boards.
    2. Filters based on keywords.
    3. Deduplicates using a hash.
    4. Embeds and stores in the vector database.
    5. Searches for the best matches.
    6. Uses MegaLLM to evaluate relevancy.
    7. Sends email notifications for matches.
    """
    logger.info("Starting Job Alert Pipeline...")
    
    # Ensure database is set up
    initialize_db()
    
    preferences = config.PREFERENCES
    if not preferences:
        logger.error("No preferences found in config.yaml. Aborting.")
        return
        
    role = preferences.get("role", "Software Engineer")
    location = preferences.get("location", "Remote")
    
    # Generate query embedding for similarity search
    query_text = f"{role} {location} {' '.join(preferences.get('skills', []))}"
    logger.info(f"Generating query embedding for: {query_text}")
    query_embedding = embed(query_text)
    
    # Step 1: Scrape across multiple portals
    jobs = scrape_jobs_universal(query=role, location=location)
    
    processed_count = 0
    new_jobs_count = 0
    
    for job in jobs:
        processed_count += 1
        
        # Step 2: Keyword Filter
        if not keyword_filter(job):
            logger.debug(f"Job filtered out by keywords: {job['title']}")
            continue
            
        # Step 3: Deduplication
        job_hash = generate_hash(job)
        if job_exists(job_hash):
            logger.debug(f"Job already exists in DB: {job['title']}")
            continue
            
        # Step 4: Embed & Store
        job["hash"] = job_hash
        job["embedding"] = embed(job.get("description", job.get("title")))
        
        insert_job(job)
        new_jobs_count += 1

    logger.info(f"Scraping complete. Processed {processed_count} jobs, {new_jobs_count} new jobs added.")
    
    if new_jobs_count == 0:
        logger.info("No new jobs to evaluate. Pipeline run complete.")
        return
        
    # Step 5: Vector Search for top candidates
    logger.info("Searching for top candidates in the database...")
    candidates = search_similar_jobs(query_embedding, top_k=10)
    
    # Step 6 & 7: LLM Evaluation and Notification
    matched_jobs = []
    for job in candidates:
        if is_relevant(job, preferences):
            matched_jobs.append(job)
            subject = f"🚀 AI Job Match: {job['title']} at {job['company']}"
            # Modern HTML Email Template
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
              body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; }}
              .container {{ max-width: 600px; background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin: auto; }}
              h1 {{ color: #2c3e50; font-size: 24px; margin-top: 0; border-bottom: 2px solid #eee; padding-bottom: 15px; }}
              .job-title {{ font-size: 22px; color: #2980b9; margin-bottom: 5px; font-weight: 600; }}
              .company-info {{ font-size: 16px; color: #7f8c8d; margin-bottom: 20px; font-weight: 500; }}
              .description {{ font-size: 15px; line-height: 1.6; color: #444; background: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin-bottom: 25px; border-radius: 0 5px 5px 0; }}
              .btn-container {{ text-align: center; margin-top: 30px; }}
              .btn {{ display: inline-block; padding: 14px 28px; background-color: #27ae60; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; transition: background-color 0.3s; }}
              .btn:hover {{ background-color: #219653; }}
              .footer {{ margin-top: 30px; font-size: 12px; color: #aaa; text-align: center; border-top: 1px solid #eee; padding-top: 15px; }}
            </style>
            </head>
            <body>
              <div class="container">
                <h1>🚀 AI Job Match Found!</h1>
                <p style="color: #555; font-size: 16px;">We found a highly relevant position matching your profile:</p>
                
                <div class="job-title">{job.get('title', 'Unknown Title')}</div>
                <div class="company-info">🏢 {job.get('company', 'Unknown')} &nbsp;|&nbsp; 📍 {job.get('location', 'Unknown')}</div>
                
                <div class="description">
                  {job.get('description', 'No description available.')}
                </div>
                
                <div class="btn-container">
                  <a href="{job.get('link', '#')}" class="btn">Go and Apply</a>
                </div>
                
                <div class="footer">
                  Powered by Job Alert Agent • MegaLLM
                </div>
              </div>
            </body>
            </html>
            """
                   
            send_email(subject=subject, body=html_body, is_html=True)

    logger.info(f"Pipeline complete. Found {len(matched_jobs)} highly relevant jobs.")
