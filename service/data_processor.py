# app/data_processing/data_processor.py

import json
from typing import List, Dict
from collections import defaultdict
import re

class DataProcessor:
    """
    Class for processing scraped data.
    """

    def clean_text(self, text: str) -> str:
        """
        Clean the text if necessary.

        :param text: The text to clean.
        :return: The cleaned text.
        """
        # Implement text cleaning logic if necessary
        return text

    def split_text(self, text: str, max_length: int = 500) -> List[str]:
        """
        Split text into chunks.

        :param text: The text to split.
        :param max_length: Maximum number of words per chunk.
        :return: List of text chunks.
        """
        words = text.split()
        chunks = []
        for i in range(0, len(words), max_length):
            chunk = ' '.join(words[i:i + max_length])
            chunks.append(chunk)
        return chunks

    def process_data(self, scraped_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Process the scraped data.

        :param scraped_data: List of dictionaries containing scraped data.
        :return: Processed data.
        """
        processed_data = []
        for item in scraped_data:
            cleaned_text = self.clean_text(item['text'])
            text_chunks = self.split_text(cleaned_text)
            for chunk in text_chunks:
                processed_data.append({'url': item['url'], 'text': chunk})
        return processed_data

    def save_processed_data(self, processed_data: List[Dict[str, str]], filename: str = 'processed_data.json'):
        """
        Save the processed data to a JSON file.

        :param processed_data: The processed data to save.
        :param filename: The filename to save to.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=4)

    def create_numerical_index(self, processed_data: List[Dict[str, str]]) -> Dict[str, List[int]]:
        """
        Create an inverted index for numerical values.

        :param processed_data: The processed data.
        :return: A dictionary mapping numerical values to list of indices.
        """
        numerical_index = defaultdict(list)
        for idx, item  in enumerate(processed_data):
            numbers = re.findall(r'\b\d+\.?\d*%', item['text'])
            numbers += re.findall(r'\b\d+\.?\d*\b', item['text'])
            for number in numbers:
                numerical_index[number].append(idx)
        return numerical_index        
