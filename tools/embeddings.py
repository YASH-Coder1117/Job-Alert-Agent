from typing import List
from sentence_transformers import SentenceTransformer
from config.config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class EmbeddingModel:
    _instance = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if cls._instance is None:
            logger.info(f"Loading embedding model: {config.EMBEDDING_MODEL}")
            cls._instance = SentenceTransformer(config.EMBEDDING_MODEL)
            logger.info("Embedding model loaded successfully.")
        return cls._instance

def embed(text: str) -> List[float]:
    """
    Generates an embedding vector for the given text.
    
    Args:
        text (str): The input string to embed.
        
    Returns:
        List[float]: A list of floats representing the text embedding.
    """
    try:
        model = EmbeddingModel.get_model()
        return model.encode(text).tolist()
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        # Return a dummy vector of 384 zeros to prevent pipeline crash if embedding fails
        return [0.0] * 384
