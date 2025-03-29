from azure.cosmos import CosmosClient, PartitionKey, exceptions
from src.document_loader import document_loader
from src.git_helper import git_helper
from langchain_openai import OpenAIEmbeddings
import os
import random
from dotenv import load_dotenv
load_dotenv()

EMBEDDING_MODEL="text-embedding-ada-002"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COSMOS_URL = os.getenv("COSMOS_URL")
COSMOS_KEY = os.getenv("COSMOS_KEY")

client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY )
database_name = "MyDatabase"
container_name = "docs"
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

openai_embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=OPENAI_API_KEY
)

print("Cloning or updating GitHub repository...")
git_helper()

print("Loading documents...")
doc_loader = document_loader()
documents = doc_loader.load_documents()
sliced_documents = doc_loader.split_documents(documents) 

file_name = {}
n=0
for doc in sliced_documents:
    title = doc.metadata['source']
    content = doc.page_content
    embed = openai_embeddings.embed_query(title + " " + content)
    page_num = None
    
    if title in file_name:
        page_num = file_name[title] + 1  
    else:
        page_num = 1
        file_name[title] = page_num 
        
    document = {
        "filename": title.replace("data/", ""),
        "page": page_num,
        "content": content,
        "vector": embed,
        "id": str(random.randint(999999999, 9999999999)),
    }
    try:
        container.create_item(body=document)
        print(f"{title} {page_num} added successfully.")
    except exceptions.CosmosHttpResponseError as e:
        print(f"Failed to add book '{title}': {e.message}")