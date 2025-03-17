# # app/chatbot/chatbot.py

# import openai
from typing import Tuple
import re
from groq import Groq


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
#     def get_response(self, question: str) -> Tuple[str, bool, float]:

#         numerical_values = re.findall(r'\b\d+\.?\d*%', question)
#         numerical_values += re.findall(r'\b\d+\.?\d*\b', question)

#         question_embedding = self.embedding_generator.generate_embeddings([question])[0]

#         metadata_filter = None
#         if numerical_values:

#             metadata_filter = {
#                 "numerical_values": {"$in": numerical_values}
#             }

#         matches = self.pinecone_manager.query(
#             vector=question_embedding,

#             top_k=5,
#             filter=metadata_filter
#         )

#         relevant_texts = [match['metadata']['text'] for match in matches['matches']]
#         prompt = "Answer the following question based on the provided information:\n\n"
#         for text in relevant_texts:
#             prompt += f"- {text}\n"
#         prompt += f"\nQuestion: {question}\nAnswer:"


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
import asyncio
import aiohttp


import re
import requests


class Chatbot:
    def __init__(
            self,
            pinecone_manager,
            embedding_generator,
            base_url="http://localhost:11434/v1/chat/completions", 
            model_name="llama3.2:1b"
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
        # prompt = "Answer the following question based on the provided information:\n\n"
        system_prompts = []
        for text in relevant_texts:
            # prompt += f"- {text}\n"
            # print(f"- {text}\n")
            system_prompts.append(
                {
                    "role": "system",
                    "content": text
                }
            )
        # prompt += f"\nQuestion: {user_qury}\nAnswer:"
        
        system_prompt = (
            "You are an assistant chatbot. Your name is Defonic\n"
            f"Question: {user_qury}.\n Analyze this question and detect the language and alphabet, then rewrite your response in the same language and alphabet. "
            # "If the user asks 'Кимсан?', 'Нимасан?', 'Кимсан' or 'Нимасан' (savol 'Who are you?' ning Uzbek kirill yozuvidagi variantlari), do not use these terms in your responses and answer in Uzbek Cyrillic. "
            # "!!! When questions are asked in Uzbek Cyrillic, the response must be in Uzbek Cyrillic. "
            # "!!! When questions are asked in Russian Latin, the response must be in Russian Cyrillic. "
            # "!!! When questions are asked in Russian, the response must be in Russian. "
            # "!!! When questions are asked in Uzbek Latin, the response must be in Uzbek Latin. "
            "You are an assistant for O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI. "
            # "You should not have access to personal user information such as name or surname. "
            # "Only respond to questions related to the National Statistics Committee. Do not request personal information from the user. "
            # "The user may write using either the Cyrillic or Latin alphabet in Uzbek or Russian. "
            # "Ignore punctuation marks, especially question marks, as the user may not always use them properly. "
            # "Always respond in the same alphabet and language that the user used. "
            # "If the user writes in Cyrillic, respond in Cyrillic (whether the language is Russian or Uzbek). "
            # "If the user writes in Latin, respond in Latin (whether the language is Russian or Uzbek). "
            "The organization is known as 'O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI'."
        )

        messages = [
            {"role": "system", "content": "You are an assistant chatbot. Your name is StatAI. You are an assistant for O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI. The organization is known as 'O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI'."},
            {"role": "user", "content": user_qury},
            {"role": "user", "content": "Answer only English language. "},
            {"role": "user", "content": "Answer the following question based on the provided information:"},
        ] + system_prompts 
        print("Ready chat messages: ", messages)
        try:
            response = self.invoke(messages)
            print("Response from invoke ollama", response)
          
            return {"content": response.get("content", "Kechirasiz, javob bera olmadim.")}

        except Exception as e:
            print("Ollama modelida xatolik:", e)
            raise e


    def invoke(self, messages):
        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "model": self.model_name,
                "messages": messages
            }

            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            return {"content": response.json()["choices"][0]["message"]["content"]}

        except Exception as e:
            print("Ollama modelida xatolik:", e)
            raise e
