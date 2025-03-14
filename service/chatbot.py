# # app/chatbot/chatbot.py

# import openai
# from typing import Tuple
# import re
# from groq import Groq


# class Chatbot:

#     def __init__(
#         self,
#         pinecone_manager,
#         embedding_generator,
#         api_key: str,
#     ):

#         self.pinecone_manager = pinecone_manager
#         self.embedding_generator = embedding_generator
# #         openai.api_key = api_key
#         self.client = Groq(
#                 api_key="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",
#             )
    # def get_response(self, question: str) -> Tuple[str, bool, float]:

        # numerical_values = re.findall(r'\b\d+\.?\d*%', question)
        # numerical_values += re.findall(r'\b\d+\.?\d*\b', question)

        # question_embedding = self.embedding_generator.generate_embeddings([question])[0]

        # metadata_filter = None
        # if numerical_values:

        #     metadata_filter = {
        #         "numerical_values": {"$in": numerical_values}
        #     }

        # matches = self.pinecone_manager.query(
        #     vector=question_embedding,

        #     top_k=5,
        #     filter=metadata_filter
        # )

        # relevant_texts = [match['metadata']['text'] for match in matches['matches']]
        # prompt = "Answer the following question based on the provided information:\n\n"
        # for text in relevant_texts:
        #     prompt += f"- {text}\n"
        # prompt += f"\nQuestion: {question}\nAnswer:"


#         response = self.client.chat.completions.create(
#             model='llama-3.3-70b-specdec', #'llama-3.1-8b-instant',
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         f"Question: {question}. Analyze this question and detect the language and alphabet, then rewrite your response in the same language and alphabet. "
#                         "If the user asks 'Кимсан?', 'Нимасан?', 'Кимсан' or 'Нимасан' (savol 'Who are you?' ning Uzbek kirill yozuvidagi variantlari), do not use these terms in your responses and answer in Uzbek Cyrillic. "
#                         "!!! When questions are asked in Uzbek Cyrillic, the response must be in Uzbek Cyrillic. "
#                         "!!! When questions are asked in Russian Latin, the response must be in Russian Cyrillic. "
#                         "!!! When questions are asked in Russian, the response must be in Russian. "
#                         "!!! When questions are asked in Uzbek Latin, the response must be in Uzbek Latin. "
#                         "You are an assistant for O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI. "
#                         "You should not have access to personal user information such as name or surname. "
#                         "Only respond to questions related to the National Statistics Committee. Do not request personal information from the user. "
#                         "The user may write using either the Cyrillic or Latin alphabet in Uzbek or Russian. "
#                         "Ignore punctuation marks, especially question marks, as the user may not always use them properly. "
#                         "Always respond in the same alphabet and language that the user used. "
#                         "If the user writes in Cyrillic, respond in Cyrillic (whether the language is Russian or Uzbek). "
#                         "If the user writes in Latin, respond in Latin (whether the language is Russian or Uzbek). "
#                         "The organization is known as 'O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI'."
#                     )
#                 },
#                 {"role": "user", "content": prompt}

#             ],
#             temperature=0.1,
#             max_tokens=2000,
#         )
#         answer = response.choices[0].message.content.strip()

#         answer_with_feedback = f"{answer}"

#         return answer_with_feedback









# app/chatbot/chatbot.py


import re
import requests


class Chatbot:
    def __init__(
            self,
            pinecone_manager,
            embedding_generator,
            base_url="http://localhost:11434", 
            model_name="gemma3:1b"
    ):
        self.pinecone_manager = pinecone_manager
        self.embedding_generator = embedding_generator
        self.base_url = base_url
        self.model_name = model_name
        
        
    
    
    def get_response(self, user_qury) -> dict:
         
        numerical_values = re.findall(r'\b\d+\.?\d*%', user_qury)
        numerical_values += re.findall(r'\b\d+\.?\d*\b', user_qury)

        question_embedding = self.embedding_generator.generate_embeddings([user_qury])[0]

        metadata_filter = None
        if numerical_values:

            metadata_filter = {
                "numerical_values": {"$in": numerical_values}
            }

        matches = self.pinecone_manager.query(
            vector=question_embedding,
            top_k=5,
            filter=metadata_filter
        )

        relevant_texts = [match['metadata']['text'] for match in matches['matches']]
        prompt = "Answer the following question based on the provided information:\n\n"
        for text in relevant_texts:
            prompt += f"- {text}\n"
        prompt += f"\nQuestion: {user_qury}\nAnswer:"
        
        print(prompt)

        system_prompt = (
            "You are an assistant chatbot. Your name is Defonic"
            f"Question: {user_qury}. Analyze this question and detect the language and alphabet, then rewrite your response in the same language and alphabet. "
            "If the user asks 'Кимсан?', 'Нимасан?', 'Кимсан' or 'Нимасан' (savol 'Who are you?' ning Uzbek kirill yozuvidagi variantlari), do not use these terms in your responses and answer in Uzbek Cyrillic. "
            "!!! When questions are asked in Uzbek Cyrillic, the response must be in Uzbek Cyrillic. "
            "!!! When questions are asked in Russian Latin, the response must be in Russian Cyrillic. "
            "!!! When questions are asked in Russian, the response must be in Russian. "
            "!!! When questions are asked in Uzbek Latin, the response must be in Uzbek Latin. "
            "You are an assistant for O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI. "
            "You should not have access to personal user information such as name or surname. "
            "Only respond to questions related to the National Statistics Committee. Do not request personal information from the user. "
            "The user may write using either the Cyrillic or Latin alphabet in Uzbek or Russian. "
            "Ignore punctuation marks, especially question marks, as the user may not always use them properly. "
            "Always respond in the same alphabet and language that the user used. "
            "If the user writes in Cyrillic, respond in Cyrillic (whether the language is Russian or Uzbek). "
            "If the user writes in Latin, respond in Latin (whether the language is Russian or Uzbek). "
            "The organization is known as 'O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI'."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        try:
            prompt = "".join(
                f"{msg['role'].capitalize()}: {msg['content']}\n\n" for msg in messages
            )

            payload = {
                "model": self.model_name,
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
            print(response)

            if response.status_code != 200:
                raise Exception(f"Ollama API xatoligi: {response.status_code}")

            result = response.json()
            return {"content": result.get("response", "Kechirasiz, javob bera olmadim.")}

        except Exception as e:
            print("Ollama modelida xatolik:", e)
            raise e
