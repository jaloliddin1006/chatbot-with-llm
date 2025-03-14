import requests

class OllamaModel:
    def __init__(self, base_url="http://localhost:11434", model="gemma3:1b"):
        self.base_url = base_url
        self.model = model

    def invoke(self, messages):
        try:
            prompt = "".join(
                f"{msg['role'].capitalize()}: {msg['content']}\n\n" for msg in messages
            )

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_k": 10,
                    "top_p": 0.8,
                    "repeat_penalty": 1.1,
                    "max_tokens": 300,
                    "num_threads": 4,
                },
            }

            response = requests.post(f"{self.base_url}/api/generate", json=payload)

            if response.status_code != 200:
                raise Exception(f"Ollama API xatoligi: {response.status_code}")

            result = response.json()
            return {"content": result.get("response", "Kechirasiz, javob bera olmadim.")}

        except Exception as e:
            print("Ollama modelida xatolik:", e)
            raise e



# Test qilish
if __name__ == "__main__":
    model = OllamaModel()
    messages = [
        {"role": "system", "content": "You are an assistant chatbot. Your name is Defonic"},
        {"role": "user", "content": "hi, who are you?"},
    ]
    response = model.invoke(messages)
    print(response)
