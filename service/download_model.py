
local_path = "./models/llama-3-2-1b"
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("unsloth/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("unsloth/Llama-3.2-1B")

# Lokal papkaga saqlash
model.save_pretrained(local_path)
tokenizer.save_pretrained(local_path)

print(f"Model  lokal {local_path} papkasiga saqlandi.")