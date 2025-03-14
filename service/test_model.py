import ollama

# # Model nomi
model_name = "llama3.2:3b"

# Embedding olish uchun matn
texts = [
    "Bu birinchi misol matn.",
    "Bu ikkinchi misol matn."
]

# # Embeddinglarni olish
# response = ollama.embed(
#     model=model_name,
#     input=texts
# )

# # Natijalarni chop etish
# embeddings = response["embeddings"]
# for i, embedding in enumerate(embeddings):
#     print(f"Matn {i + 1} uchun embedding (birinchi 10 ta qiymat): {embedding[:10]}")
#     print(f"Embedding uzunligi: {len(embedding)}\n")
    
    
    
from ollama import Client
client = Client(host='http://localhost:11434')
response = client.embed(model=model_name, input=texts)