from langchain_ollama import OllamaEmbeddings
from langchain.vectorstores.chroma import Chroma # type: ignore
from langchain.prompts import ChatPromptTemplate
import requests
import time

CHROMA_PATH = "chroma"
DATA_PATH = "data"

class database: 
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.embedding_model = "nomic-embed-text"
        self.ollama_base_url = "http://ollama:11434"
        
    def similarity_search_with_score(self, query_text, k=3):
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.get_embedding_function())
        return db.similarity_search_with_score(query_text, k=k)
    
    def ensure_model_exists(self):
        model_url = f"{self.ollama_base_url}/api/tags"
        try:
            response = requests.get(model_url)
            models = response.json().get('models', [])
            model_exists = any(model['name'] == self.embedding_model for model in models)
            
            if not model_exists:
                print(f"Model '{self.embedding_model}' not found. Pulling it now...")
                pull_url = f"{self.ollama_base_url}/api/pull"
                pull_response = requests.post(pull_url, json={"name": self.embedding_model})
                
                if pull_response.status_code == 200:
                    print(f"Successfully pulled model '{self.embedding_model}'")
                    # Wait a moment for the model to be fully loaded
                    time.sleep(2)
                else:
                    print(f"Failed to pull model: {pull_response.text}")
                    raise Exception(f"Failed to pull model '{self.embedding_model}'")
            else:
                print(f"Model '{self.embedding_model}' already exists")
                
        except Exception as e:
            print(f"Error checking/pulling model: {str(e)}")
            raise
        
    def get_embedding_function(self):
        # Ensure the embedding model exists before creating embeddings
        self.ensure_model_exists()
        
        embeddings = OllamaEmbeddings(
            model=self.embedding_model,
            base_url=self.ollama_base_url  # Point to the Ollama container
        )
        return embeddings
    
    def add_to_chroma(self, chunks):
        # Load the existing database.
        db = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=self.get_embedding_function()
        )

        # Calculate Page IDs.
        chunks_with_ids = self.calculate_chunk_ids(chunks)

        # Add or Update the documents.
        existing_items = db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
            db.persist()
        else:
            print("✅ No new documents to add")

    def calculate_chunk_ids(self, chunks):

        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks