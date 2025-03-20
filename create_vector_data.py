from src.document_loader import document_loader # type: ignore
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
EMBEDDING_MODEL = "text-embedding-ada-002"

def get_embedding(client, text):
    response = client.embeddings.create(
        input=text, model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

def main():
    
    print("Loading documents...")
    doc_loader = document_loader()
    documents = doc_loader.load_documents()
    sliced_documents = doc_loader.split_documents(documents) 
    
    for doc in sliced_documents[0:1000]:
        page_content = doc.page_content
        metadata = doc.metadata
        embedded=get_embedding(page_content)
        
        # embed=get_embedding(doc.page_content)
        
        # page_content = doc.page_content
        # metadata = doc.metadata
        
        # print(str(doc))
        # print("--------")
        # print(embed)
        # print("\n \n")
        

if __name__ == "__main__":
    main() 