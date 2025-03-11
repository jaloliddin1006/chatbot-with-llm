# app/embeddings/embedding_generator.py

import openai
from typing import List

class EmbeddingGenerator:
    """
    Class for generating embeddings using OpenAI's embedding API.
    """

    def __init__(self, api_key: str):
        """
        Initialize the EmbeddingGenerator.

        :param api_key: OpenAI API key.
        """
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using OpenAI's embedding API.

        :param texts: List of texts to generate embeddings for.
        :return: List of embeddings.
        """
        embeddings = []
        for text in texts:
            response = openai.Embedding.create(
                input=text,
                model='text-embedding-ada-002'  # Choose an appropriate embedding model
            )
            embeddings.append(response['data'][0]['embedding'])
        return embeddings
