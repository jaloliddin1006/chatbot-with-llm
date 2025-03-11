import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urlparse
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys


# Configure logging for this module
logger = logging.getLogger(__name__)

class WebScraper:
    """
    Class for scraping web pages and extracting text.
    """

    def __init__(self, url_list: List[str]):
        """
        Initialize the WebScraper.

        :param url_list: List of URLs to scrape.
        """
        self.url_list = url_list
        self.scraped_data = []

    def is_valid_url(self, url: str) -> bool:
        """
        Check if a URL is valid.

        :param url: The URL to check.
        :return: True if valid, False otherwise.
        """
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)

    def extract_text(self, soup: BeautifulSoup) -> str:
        """
        Extract text from a BeautifulSoup object.

        :param soup: BeautifulSoup object.
        :return: Extracted text.
        """
        # Remove unwanted elements
        for script_or_style in soup(['script', 'style', 'nav', 'footer']):
            script_or_style.decompose()
        # Extract text
        text = soup.get_text(separator=' ')
        # Clean up the text
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = ' '.join(lines)
        return text

    def scrape_url(self, url: str) -> dict:
        """
        Scrape a single URL.

        :param url: The URL to scrape.
        :return: A dictionary with the URL and extracted text.
        """
        if not self.is_valid_url(url):
            logger.warning(f"Invalid URL skipped: {url}")
            return None

        # Initialize Safari WebDriver
        try:
            logger.info(f"Initializing WebDriver for {url}")
            if sys.platform == "win32" or sys.platform == "linux":
                driver = webdriver.Chrome()
            elif sys.platform == "darwin":
                driver = webdriver.Safari()
            else:
                driver = webdriver.Safari()

            logger.info(f"WebDriver initialized successfully for {url}")
        except WebDriverException as e:
            logger.error(f"Failed to initialize Safari WebDriver for {url}: {e}", exc_info=True)
            return None

        try:
            logger.info(f"Navigating to {url}")
            driver.get(url)
            time.sleep(2)  # Adjust based on page load times
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            text = self.extract_text(soup)
            if text:
                logger.info(f"Scraped data from {url}")
                return {'url': url, 'text': text}
            else:
                logger.warning(f"No text extracted from {url}")
                return None
        except TimeoutException as e:
            logger.error(f"Timeout while scraping {url}: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}", exc_info=True)
            return None
        finally:
            logger.info(f"Closing WebDriver for {url}")
            driver.quit()

    def scrape(self):
        """
        Scrape the URLs in the url_list and extract text using multithreading.
        """
        logger.info("Starting scraping process with multithreading.")

        # Define the number of worker threads
        num_threads = min(10, len(self.url_list))  # Adjust based on your requirements

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit all scraping tasks to the thread pool
            future_to_url = {executor.submit(self.scrape_url, url.strip()): url.strip() for url in self.url_list}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        self.scraped_data.append(result)
                except Exception as e:
                    logger.error(f"Error occurred while processing {url}: {e}", exc_info=True)

        logger.info("Scraping process completed.")

    def save_scraped_data(self, filename: str = 'scraped_data.json'):
        """
        Save the scraped data to a JSON file.

        :param filename: The filename to save to.
        """
        try:
            logger.info(f"Saving scraped data to {filename}.")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_data, f, ensure_ascii=False, indent=4)
            logger.info("Scraped data saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save scraped data: {e}", exc_info=True)
