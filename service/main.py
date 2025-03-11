from .chat import pinecone_manager
import openai

index_info = pinecone_manager.index.describe_index_stats()

# print(index_info)

all_ids = index_info['namespaces'].get('', {}).get('vector_count', 0)
# print(all_ids)
query_result = pinecone_manager.index.query(vector=[0.0] * 1536, top_k=10000, include_metadata=True)
# print(query_result)
# response = openai.Embedding.create(
#                 input="Salom sizga qanday yordam kerak",
#                 model='text-embedding-ada-002'  # Choose an appropriate embedding model
# )
# print("RESPONSE: ",response)

pinecone_manager.delete_embedding(id='a')
# print(pinecone_manager)