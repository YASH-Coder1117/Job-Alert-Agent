import yaml
from src.pipeline.orchestrator import run_pipeline

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

run_pipeline(config)