from typing import List
from sentence_transformers import SentenceTransformer

# Initialize the MPNet-base-v2 model globally to reuse it across calls
_model = SentenceTransformer('all-mpnet-base-v2')

def hf_mpnet_embed(text: str) -> List[float]:
    """
    Generate embeddings for the given text using HuggingFace MPNet-base-v2 model.

    Args:
        text (str): Input text to embed.

    Returns:
        List[float]: Embedding vector.
    """
    vector = _model.encode(text, convert_to_numpy=True)
    return vector.tolist()
