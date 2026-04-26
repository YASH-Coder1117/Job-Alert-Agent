import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_yaml_config(file_path: str = "config/config.yaml") -> dict:
    """Loads YAML configuration for preferences."""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Failed to load yaml config: {e}")
        return {}

class Config:
    # Database
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    # LLM Settings
    MEGALLM_API_KEY = os.getenv("MEGALLM_API_KEY", "")
    MEGALLM_BASE_URL = os.getenv("MEGALLM_BASE_URL", "https://ai.megallm.io/v1")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-5")
    
    # Email Settings
    EMAIL_FROM = os.getenv("EMAIL_FROM", "")
    EMAIL_TO = os.getenv("EMAIL_TO", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

    # Embeddings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # Load preferences
    PREFERENCES = load_yaml_config().get("preferences", {})

config = Config()
