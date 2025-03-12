# Load model directly
from transformers import AutoModel
model = AutoModel.from_pretrained("models/Llama-3.2-1b")
print("the end")