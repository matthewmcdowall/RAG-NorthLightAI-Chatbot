from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from supabase import create_client, Client
from tqdm import tqdm
import os
import dotenv
from langchain_core.documents import Document

from parser import extract_final_urls
from scraper import scrape

# Load environment variables from .env file
dotenv.load_dotenv()




def store_to_db(website="https://northlightai.com"):

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # Clean the table before loading new data
    supabase.table("nlai_content").delete().not_.is_("id", None).execute()

    # Extract sitemap URLs
    url_list, tree = extract_final_urls(website)
    
    
    company_name = "Northlight AI"

    for link in tqdm(url_list, desc=f"Scraping & indexing ({company_name})", unit="link"):
        # Scrape the URL
        text = scrape(link)
        if not text.strip():
            continue  # skip empty pages

        # Create metadata and document content
        metadata={
                "source": str(link),
                "website": str(website)
            }

        docs = Document(
            page_content=text,
            metadata=metadata
        )
        
        # Chunking
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=500)
        chunks = text_splitter.split_documents([docs])

        # Index chunks and store in Supabase
        for chunk in chunks:
            # Generate embedding
            vector = embeddings.embed_query(chunk.page_content)

            # Insert into Supabase
            supabase.rpc("insert_webcontent_nlai", {
                "content": chunk.page_content,
                "metadata": metadata,
                "embedding": vector  # list of floats; pgvector input accepted here
            }).execute()
