# # app/chatbot/chatbot.py

import openai
from typing import Tuple
import re
from groq import Groq


class Chatbot:

    def __init__(
        self,
        pinecone_manager,
        embedding_generator,
        api_key: str,
    ):

        self.pinecone_manager = pinecone_manager
        self.embedding_generator = embedding_generator
#         openai.api_key = api_key
        self.client = Groq(
                api_key="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",
            )
    def get_response(self, question: str) -> Tuple[str, bool, float]:

        numerical_values = re.findall(r'\b\d+\.?\d*%', question)
        numerical_values += re.findall(r'\b\d+\.?\d*\b', question)

        question_embedding = self.embedding_generator.generate_embeddings([question])[0]

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
        prompt += f"\nQuestion: {question}\nAnswer:"


        response = self.client.chat.completions.create(
            model='llama-3.3-70b-specdec', #'llama-3.1-8b-instant',
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Question: {question}. Analyze this question and detect the language and alphabet, then rewrite your response in the same language and alphabet. "
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
                },
                {"role": "user", "content": prompt}

            ],
            temperature=0.1,
            max_tokens=2000,
        )
        answer = response.choices[0].message.content.strip()

        answer_with_feedback = f"{answer}"

        return answer_with_feedback




# import os
#
# from groq import Groq
#
# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )
#
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama-3.1-8b-instant",
# )
#
# print(chat_completion.choices[0].message.content)


# app/chatbot/chatbot.py

#
# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from typing import Tuple
# import re
#
#
# class Chatbot:
#     def __init__(
#             self,
#             pinecone_manager,
#             embedding_generator,
#             model_path: str = "models/llama-3.2-1b",  # Lokal papka yo‘li
#     ):
#         self.pinecone_manager = pinecone_manager
#         self.embedding_generator = embedding_generator
#
#         # Model va tokenizer lokal papkadan yuklanadi
#         self.model = AutoModelForCausalLM.from_pretrained(model_path)
#         self.tokenizer = AutoTokenizer.from_pretrained(model_path)
#
#         # Modelni GPU ga o‘tkazish (agar mavjud bo‘lsa)
#         if torch.cuda.is_available():
#             self.model = self.model.to("cuda")
#
#     def generate_response(self, prompt: str) -> str:
#         # Promptni tokenlarga aylantirish
#         inputs = self.tokenizer(prompt, return_tensors="pt")
#
#         # Agar GPU mavjud bo‘lsa, inputlarni GPU ga o‘tkazish
#         if torch.cuda.is_available():
#             inputs = {key: val.to("cuda") for key, val in inputs.items()}
#
#         # Javob generatsiyasi
#         outputs = self.model.generate(
#             **inputs,
#             max_length=8000,  # Maksimal tokenlar soni
#             temperature=0.1,  # Tasodifiylik darajasi
#             do_sample=True,  # Tasodifiy tanlash
#         )
#
#         # Tokenlarni matnga aylantirish
#         answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return answer.strip()
#
#     def get_response(self, question: str) -> Tuple[str, bool, float]:
#         # Savoldan raqamli qiymatlarni ajratib olish
#         numerical_values = re.findall(r'\b\d+\.?\d*%', question)
#         numerical_values += re.findall(r'\b\d+\.?\d*\b', question)
#
#         # Savol embeddingini generatsiya qilish
#         question_embedding = self.embedding_generator.generate_embeddings([question])[0]
#
#         # Metadata filtri
#         metadata_filter = None
#         if numerical_values:
#             metadata_filter = {
#                 "numerical_values": {"$in": numerical_values}
#             }
#
#         # Pinecone dan mos keladigan ma'lumotlarni olish
#         matches = self.pinecone_manager.query(
#             vector=question_embedding,
#             top_k=5,
#             filter=metadata_filter
#         )
#
#         # Relevant matnlarni yig‘ish
#         relevant_texts = [match['metadata']['text'] for match in matches['matches']]
#         prompt = "Answer the following question based on the provided information:\n\n"
#         for text in relevant_texts:
#             prompt += f"- {text}\n"
#         prompt += f"\nQuestion: {question}\nAnswer:"
#
#         # System prompt qo‘shish
#         system_prompt = (
#             f"Question: {question}. Analyze this question and detect the language and alphabet, then rewrite your response in the same language and alphabet. "
#             "If the user asks 'Кимсан?', 'Нимасан?', 'Кимсан' or 'Нимасан' (savol 'Who are you?' ning Uzbek kirill yozuvidagi variantlari), do not use these terms in your responses and answer in Uzbek Cyrillic. "
#             "!!! When questions are asked in Uzbek Cyrillic, the response must be in Uzbek Cyrillic. "
#             "!!! When questions are asked in Russian Latin, the response must be in Russian Cyrillic. "
#             "!!! When questions are asked in Russian, the response must be in Russian. "
#             "!!! When questions are asked in Uzbek Latin, the response must be in Uzbek Latin. "
#             "You are an assistant for O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI. "
#             "You should not have access to personal user information such as name or surname. "
#             "Only respond to questions related to the National Statistics Committee. Do not request personal information from the user. "
#             "The user may write using either the Cyrillic or Latin alphabet in Uzbek or Russian. "
#             "Ignore punctuation marks, especially question marks, as the user may not always use them properly. "
#             "Always respond in the same alphabet and language that the user used. "
#             "If the user writes in Cyrillic, respond in Cyrillic (whether the language is Russian or Uzbek). "
#             "If the user writes in Latin, respond in Latin (whether the language is Russian or Uzbek). "
#             "The organization is known as 'O‘ZBEKISTON RESPUBLIKASI MILLIY STATISTIKA QO‘MITASI'."
#         )
#
#         # To‘liq promptni tayyorlash
#         full_prompt = f"{system_prompt}\n\n{prompt}"
#
#         # Modeldan javob olish
#         answer = self.generate_response(full_prompt)
#
#         # Javobni qaytarish
#         answer_with_feedback = f"{answer}"
#         return answer_with_feedback, True, 0.95  # Soxta qiymatlar, agar kerak bo‘lsa o‘zgartiring
#
