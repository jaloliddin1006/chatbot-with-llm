# app/vector_store/pinecone_manager.py

import logging
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeException
from .config import Config

class PineconeManager:
    def __init__(self):
        # Initialize Pinecone by creating an instance of the Pinecone class
        try:
            self.pc = Pinecone(
                api_key=Config.PINECONE_API_KEY,
                environment=Config.PINECONE_ENVIRONMENT
            )
            logging.info("Pinecone initialized successfully.")
        except PineconeException as e:
            logging.error(f"Failed to initialize Pinecone: {e}")
            raise e

        # Define index parameters
        self.index_name = 'chatbot'
        self.dimension = 1024  # Embedding dimension
        self.metric = 'cosine'  # or 'euclidean'

        # Retrieve existing indexes using the Pinecone instance
        try:
            indexes = self.pc.list_indexes().names()
            # print(f"List indexes response: {indexes}")
            logging.debug(f"List indexes response: {indexes}")
            logging.info(f"Existing indexes: {indexes}")

            # Create index if it doesn't exist
            if self.index_name not in indexes:
                logging.info(f"Creating Pinecone index '{self.index_name}'.")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric=self.metric,
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'  # Ensure this matches your Pinecone environment
                    )
                )
                logging.info(f"Pinecone index '{self.index_name}' created successfully.")
            else:
                logging.info(f"Pinecone index '{self.index_name}' already exists.")

        except PineconeException as e:
            logging.error(f"Failed to list or create Pinecone indexes: {e}")
            raise e

        # Connect to the index
        try:
            self.index = self.pc.Index(self.index_name)
            logging.info(f"Connected to Pinecone index '{self.index_name}'.")
        except PineconeException as e:
            logging.error(f"Failed to connect to Pinecone index '{self.index_name}': {e}")
            raise e

    def index_has_data(self):
        """
        Check if the Pinecone index already contains data.
        """
        try:
            index_stats = self.index.describe_index_stats()
            total_vector_count = index_stats.get('total_vector_count', 0)
            # print(f"Pinecone index '{self.index_name}' has {total_vector_count} vectors.")
            logging.debug(f"Pinecone index '{self.index_name}' has {total_vector_count} vectors.")
            return total_vector_count > 0
        except PineconeException as e:
            logging.error(f"Failed to retrieve index stats: {e}")
            return False

    def upsert_embeddings(self, ids, embeddings, metadatas, batch_size=100):
        """
        Upsert embeddings into Pinecone in batches to avoid payload size limits.
        """
        vectors = []
        for id, embedding, metadata in zip(ids, embeddings, metadatas):
            vectors.append({
                'id': id,
                'values': embedding,
                'metadata': metadata
            })

        total_vectors = len(vectors)
        logging.info(f"Total vectors to upsert: {total_vectors}")
        i = 0

        while i < total_vectors:
            current_batch_size = batch_size
            while True:
                batch = vectors[i:i + current_batch_size]
                if not batch:
                    break  # No more data

                try:
                    # Upsert the batch to the Pinecone index using the instance method
                    self.index.upsert(vectors=batch)
                    logging.info(f"Successfully upserted batch starting at index {i}.")
                    break  # Exit the inner while loop after successful upsert
                except PineconeException as e:
                    logging.error(f"Failed to upsert batch starting at index {i}: {e}")
                    # Optionally, implement retry logic here
                    raise e  # Re-raise exception after logging

            # Move to the next batch
            i += current_batch_size

    def delete_embedding(self,id):
        
        try:
            logging.info(f"ID : {id} data deleted from Pinecone")
            print(f"ID : {id} data deleted from Pinecone")
            self.index.delete(ids=[str(id)])
        except PineconeException as e:
            logging.info(f"ID : {id} data didn't deleted because of {e}")
            print(f"ID : {id} data didn't deleted because of {e}") 

    def query(self, vector, top_k=10, filter=None):
        """
        Query the Pinecone index with a given vector.
        """
        try:
            response = self.index.query(
                vector=vector,
                top_k=top_k,
                filter=filter,
                include_metadata=True
            )
            return response
        except PineconeException as e:
            logging.error(f"Failed to query Pinecone index: {e}")
            return None
