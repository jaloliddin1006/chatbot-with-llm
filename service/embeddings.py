# # app/embeddings/embedding_generator.py

# import openai
# from typing import List

# class EmbeddingGenerator:
#     """
#     Class for generating embeddings using OpenAI's embedding API.
#     """

#     def __init__(self, api_key: str):
#         """
#         Initialize the EmbeddingGenerator.

#         :param api_key: OpenAI API key.
#         """
#         self.api_key = api_key
#         openai.api_key = self.api_key

#     def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
#         """
#         Generate embeddings for a list of texts using OpenAI's embedding API.

#         :param texts: List of texts to generate embeddings for.
#         :return: List of embeddings.
#         """
#         embeddings = []
#         for text in texts:
#             response = openai.Embedding.create(
#                 input=text,
#                 model='text-embedding-ada-002'  # Choose an appropriate embedding model
#             )
#             embeddings.append(response['data'][0]['embedding'])
#         return embeddings



import requests
from typing import List

class EmbeddingGenerator:
    """
    Ollama API'si orqali LLaMA 3.2:3b modelidan foydalanib, matnlar uchun embeddinglar yaratish sinfi.
    """

    def __init__(self, model_name: str, base_url: str):
        """
        EmbeddingGenerator ni inicializatsiya qilish.

        :param model_name: Model nomi (masalan, "llama3.2:3b").
        :param base_url: Ollama API'sining asosiy URL manzili.
        """
        self.model_name = model_name
        self.base_url = base_url

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Bir nechta matn uchun embeddinglar yaratish.

        :param texts: Embeddinglari yaratiladigan matnlar ro'yxati.
        :return: Embeddinglar ro'yxati.
        """
        embeddings = []
        for text in texts:
            response = self._get_embedding_from_ollama(text)
            if response and 'embedding' in response:
                embeddings.append(response['embedding'])
            else:
                embeddings.append([])  # Agar embedding topilmasa, bo'sh ro'yhat qaytariladi
        return embeddings

    def _get_embedding_from_ollama(self, text: str) -> dict:
        """
        Ollama API'siga so'rov yuborib, matn uchun embedding olish.

        :param text: Embedding olinadigan matn.
        :return: Embeddingni o'z ichiga olgan javob.
        """
        url = f"{self.base_url}/v1/embeddings"
        payload = {
            "model": self.model_name,
            "input": text
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Agar xato bo'lsa, xatolikni ko'rsatadi
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Embedding olishda xato: {e}")
            return {}
