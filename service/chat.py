from .chatbot import Chatbot
from .config import *
from .embeddings import *
from .pinecone_manager import *
from .scrapper import *
from .data_processor import *



openai_api_key = Config.OPENAI_API_KEY
pinecone_api_key = Config.PINECONE_API_KEY
pinecone_environment = Config.PINECONE_ENVIRONMENT


if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

if not pinecone_api_key or not pinecone_environment:
    raise ValueError("Pinecone API key or environment is not set. Please set the PINECONE_API_KEY and PINECONE_ENVIRONMENT environment variables.")

# Initialize the embedding generator
embedding_generator = EmbeddingGenerator(api_key=openai_api_key)

# Initialize Pinecone manager
pinecone_manager = PineconeManager()

# Check if the Pinecone index already has data
if pinecone_manager.index_has_data():
    pass
else:
    # Ensure data directory exists
    data_dir = os.getenv('DATA_DIR', './data')
    os.makedirs(data_dir, exist_ok=True)

    # Use the URL list from Config
    url_list = Config.URL_LIST

    # Initialize and run the scraper
    scraper = WebScraper(url_list=url_list)
    scraper.scrape()
    scraped_data = scraper.scraped_data
    scraper.save_scraped_data(os.path.join(data_dir, 'scraped_data.json'))

    # Process the data
    processor = DataProcessor()
    processed_data = processor.process_data(scraped_data)
    # Save processed data if needed for debugging or future reference
    processed_data_path = os.path.join(data_dir, 'processed_data.json')
    processor.save_processed_data(processed_data, processed_data_path)

    # Prepare data for indexing
    texts = [item['text'] for item in processed_data]
    embeddings = embedding_generator.generate_embeddings(texts)
    # Prepare metadata (including numerical values)
    print("EMBEDDING : ",embeddings)
    metadatas = []

    for idx, item in enumerate(processed_data):
        text = item['text']
        # Extract numerical values from text
        numerical_values = re.findall(r'\b\d+\.?\d*%', text)
        numerical_values += re.findall(r'\b\d+\.?\d*\b', text)
        # Prepare metadata
        metadata = {
            'text': text,
            'numerical_values': numerical_values
        }
        metadatas.append(metadata)
                    # Index data into Pinecone
    ids = [str(i) for i in range(len(texts))]
    pinecone_manager.upsert_embeddings(ids, embeddings, metadatas)
    index_info = pinecone_manager.index.describe_index_stats()



# chatbot = Chatbot(pinecone_manager, embedding_generator, api_key=openai_api_key)

chatbot = Chatbot(pinecone_manager, embedding_generator)
