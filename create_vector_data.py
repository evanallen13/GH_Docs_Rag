from src.document_loader import document_loader # type: ignore
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
EMBEDDING_MODEL = "text-embedding-ada-002"

def get_embedding(text):
    response = client.embeddings.create(
        input=text, model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

def main():
    
    print("Loading documents...")
    doc_loader = document_loader()
    documents = doc_loader.load_documents()
    sliced_documents = doc_loader.split_documents(documents) 
    
    
    for doc in sliced_documents[0:10]:
        embed=get_embedding("This is a test")
        print(str(doc))
        print("--------")
        print(embed)
        print("\n \n")
        

if __name__ == "__main__":
    main() 