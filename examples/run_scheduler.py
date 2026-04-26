import time
import schedule
import sys
import os

# Ensure the parent directory is in the sys.path so we can import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import run_pipeline
from utils.logger import get_logger

logger = get_logger(__name__)

def job():
    """Wrapper function to run the pipeline and handle any top-level errors."""
    logger.info("=== Scheduler triggered Job Alert Pipeline ===")
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"Pipeline crashed during scheduled run: {e}")
    logger.info("=== Scheduled Run Complete ===")

def main():
    logger.info("Starting Job Alert Scheduler...")
    
    # Run it immediately once on startup
    job()
    
    # Schedule the job to run every 5 minutes
    # You can easily change this to .minutes, .hours, or .days
    schedule.every(5).minutes.do(job)
    
    logger.info("Scheduler is now running in the background. Press Ctrl+C to exit.")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60) # Wait a minute before checking the schedule again

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Scheduler manually stopped.")
