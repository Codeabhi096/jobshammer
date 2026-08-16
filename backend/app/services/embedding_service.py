from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """
    Given a text string, returns its embedding vector (numpy array).
    """
    return model.encode(text)