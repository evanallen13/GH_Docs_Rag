from src.git_helper import git_helper
from src.document_loader import document_loader # type: ignore
from src.database import database
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "gemma3:1b" # Find available models here https://ollama.com/library

def main():
    print("Cloning or updating GitHub repository...")
    # git_helper() # clone or update the GitHub repository
    
    print("Loading documents...")
    doc_loader = document_loader()
    documents = doc_loader.load_documents()
    sliced_documents = doc_loader.split_documents(documents) 
    
    print("Adding documents to database...")
    db = database("database")

    print("Add first 5000 documents to database...")
    db.add_to_chroma(sliced_documents[1:5000])
    print("Add last 5000 documents to database...")
    db.add_to_chroma(sliced_documents[5000:10000])
    
    llm = llama(OLLAMA_HOST, MODEL)

if __name__ == "__main__":
    main() 