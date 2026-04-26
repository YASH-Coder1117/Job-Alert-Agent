import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import run_pipeline

if __name__ == "__main__":
    print("Starting Job Alert Agent from Example Script...")
    run_pipeline()
    print("Execution Finished.")
