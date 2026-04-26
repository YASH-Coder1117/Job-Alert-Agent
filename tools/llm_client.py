from openai import OpenAI
from config.config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class MegaLLMClient:
    """Client for interacting with the MegaLLM API using the OpenAI SDK pattern."""
    
    _client = None

    @classmethod
    def get_client(cls) -> OpenAI:
        if cls._client is None:
            if not config.MEGALLM_API_KEY:
                logger.warning("MEGALLM_API_KEY is not set. LLM requests may fail.")
            
            cls._client = OpenAI(
                base_url=config.MEGALLM_BASE_URL,
                api_key=config.MEGALLM_API_KEY
            )
        return cls._client

def generate_completion(prompt: str) -> str:
    """
    Generates a text completion using the MegaLLM local model.
    
    Args:
        prompt (str): The user prompt to send to the LLM.
        
    Returns:
        str: The generated text from the model.
    """
    client = MegaLLMClient.get_client()
    
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1 # Keep temperature low for deterministic evaluation
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Failed to generate LLM completion: {e}")
        return ""
