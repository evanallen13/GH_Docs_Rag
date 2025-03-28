from src.git_helper import git_helper
from src.document_loader import document_loader # type: ignore
from src.database import database
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
from src.llama import llama
import time
from openai import OpenAI
from dotenv import load_dotenv

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "gemma3:1b" # Find available models here https://ollama.com/library

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
    print("Cloning or updating GitHub repository...")
    # git_helper() # clone or update the GitHub repository
    
    print("Loading documents...")
    doc_loader = document_loader()
    documents = doc_loader.load_documents()
    sliced_documents = doc_loader.split_documents(documents) 
    
    embed=get_embedding("This is a test")
    print(sliced_documents[0])
    print("--------")
    print(embed)
    

    # for i in sliced_documents[0:10]:
    #     with open("Output.txt", "a") as text_file:
    #         text_file.write(str(i))
    #         text_file.write("\n--------\n")

    print("Adding documents to database...")
    # db = database("database")
    
    # db.add_to_chroma(sliced_documents[:100])
    
    # for i in sliced_documents:
    #     db.add_to_chroma([i])
    #     time.sleep(.5)
        
    # start = 0
    # end = 0

    # while end < len(sliced_documents):
    #     end += 5
    #     if end > len(sliced_documents):
    #         end = len(sliced_documents)
        
    #     db.add_to_chroma(sliced_documents[start:end])
    #     start = end 

    #     time.sleep(.1)


    # llm = llama(OLLAMA_HOST, MODEL)
    
    # prompt = "What happens if you land on a property in Monopoly that you can't afford?"
    # results = db.similarity_search_with_score(prompt, k=3)
    
    # print(results)

if __name__ == "__main__":
    main() 