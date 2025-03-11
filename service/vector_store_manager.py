# app/vector_store/vector_store_manager.py

import faiss
import numpy as np
from typing import Tuple

class VectorStoreManager:
    """
    Class for managing a vector store using FAISS.
    """

    def __init__(self, embeddings: np.ndarray):
        """
        Initialize the VectorStoreManager.

        :param embeddings: NumPy array of embeddings to add to the vector store.
        """
        self.dimension = embeddings.shape[1]
        # Use IndexFlatIP for inner product (dot product)
        self.index = faiss.IndexFlatIP(self.dimension)
        # Normalize embeddings (since we're using inner product for cosine similarity)
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Search for similar embeddings in the vector store.

        :param query_embedding: The query embedding.
        :param top_k: Number of top results to return.
        :return: Distances and indices of the top results.
        """
        # Normalize query embedding
        faiss.normalize_L2(query_embedding.reshape(1, -1))
        distances, indices = self.index.search(np.array([query_embedding]), top_k)
        return distances, indices
