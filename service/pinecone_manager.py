import logging
import os
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeException
from .config import Config

class PineconeManager:
    def __init__(self):
        try:
            self.pc = Pinecone(
                api_key=Config.PINECONE_API_KEY,
                environment=Config.PINECONE_ENVIRONMENT
            )
            logging.info("Pinecone muvaffaqiyatli inicializatsiya qilindi.")
        except PineconeException as e:
            logging.error(f"Pinecone inicializatsiya qilishda xato: {e}")
            raise e

        self.index_name = 'chatbot'
        self.dimension = 1024  # Embedding o'lchami
        self.metric = 'cosine'

        try:
            indexes = self.pc.list_indexes().names()
            logging.debug(f"Mavjud indekslar: {indexes}")

            if self.index_name not in indexes:
                logging.info(f"Pinecone indeksini yaratilyapti: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric=self.metric,
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                logging.info(f"Pinecone indeks '{self.index_name}' muvaffaqiyatli yaratildi.")
            else:
                logging.info(f"Pinecone indeks '{self.index_name}' mavjud.")

        except PineconeException as e:
            logging.error(f"Pinecone indekslarini ro'yxatlash yoki yaratishda xato: {e}")
            raise e

        try:
            self.index = self.pc.Index(self.index_name)
            logging.info(f"Pinecone indeksiga ulanish muvaffaqiyatli: {self.index_name}")
        except PineconeException as e:
            logging.error(f"Pinecone indeksiga ulanishda xato: {e}")
            raise e

    def index_has_data(self):
        try:
            index_stats = self.index.describe_index_stats()
            total_vector_count = index_stats.get('total_vector_count', 0)
            logging.debug(f"Indeksda jami {total_vector_count} vektor mavjud.")
            return total_vector_count > 0
        except PineconeException as e:
            logging.error(f"Indeks statistikalarini olishda xato: {e}")
            return False

    def upsert_embeddings(self, ids, embeddings, metadatas, batch_size=100):
        vectors = [{
            'id': id,
            'values': embedding,
            'metadata': metadata
        } for id, embedding, metadata in zip(ids, embeddings, metadatas)]

        total_vectors = len(vectors)
        logging.info(f"Qo'shiladigan vektorlar soni: {total_vectors}")
        i = 0
        while i < total_vectors:
            current_batch_size = batch_size
            while True:
                batch = vectors[i:i + current_batch_size]
                if not batch:
                    break

                try:
                    self.index.upsert(vectors=batch)
                    logging.info(f"Batch {i}-indexdan boshlab muvaffaqiyatli qo'shildi.")
                    break
                except PineconeException as e:
                    logging.error(f"Batch {i}-indexdan boshlab qo'shishda xato: {e}")
                    break

            i += current_batch_size

    def delete_embedding(self, id):
        try:
            self.index.delete(ids=[str(id)])
            logging.info(f"ID {id} bo'yicha ma'lumotlar o'chirildi.")
        except PineconeException as e:
            logging.error(f"ID {id} bo'yicha ma'lumotlarni o'chirishda xato: {e}")

    def query(self, vector, top_k=10, filter=None):
        try:
            response = self.index.query(
                vector=vector,
                top_k=top_k,
                filter=filter,
                include_metadata=True
            )
            return response
        except PineconeException as e:
            logging.error(f"Pinecone indeksiga so'rov yuborishda xato: {e}")
            return None
