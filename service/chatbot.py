# app/chatbot/chatbot.py

import openai
from typing import Tuple
import re

from datetime import datetime
import requests
import pandas as pd
from io import StringIO


def get_currency():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = "https://brb.uz"
    req = requests.get(url)
    df_list = pd.read_html(StringIO(req.text))

    physical = df_list[0].to_string(index=False, header=True)
    legal = df_list[1].to_string(index=False, header=True)

    text = f"""
<b>{now} vaqtiga ko'ra valyutalar kursi:</b>\n\n
<b>Jismoniy shaxslarga uchun:</b>\n
<pre>{physical}</pre>\n
<b>Yuridik shaxslar uchun:</b>\n
<pre>{legal}</pre>
    """
    return text


class Chatbot:

    def __init__(
        self,
        pinecone_manager,
        embedding_generator,
        api_key: str,
    ):

        self.pinecone_manager = pinecone_manager
        self.embedding_generator = embedding_generator
        openai.api_key = api_key

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
        

        # currecncy = get_currency()
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini',
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
            max_tokens=1000,
        )
        answer = response['choices'][0]['message']['content'].strip()        

        answer_with_feedback = f"{answer}"

        return answer_with_feedback
