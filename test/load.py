from azure.cosmos import CosmosClient, PartitionKey, exceptions
from src.document_loader import document_loader # type: ignore
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
container_name = "bookstore"
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

openai_embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=OPENAI_API_KEY
)

print("Loading documents...")
doc_loader = document_loader()
documents = doc_loader.load_documents()
sliced_documents = doc_loader.split_documents(documents) 
    

# def add_book(container, book_id, isbn, title, description, author, content_vector):
#     book = {
#         "id": book_id,
#         "title": title,
#         "isbn": isbn,
#         "author": author,
#         "description": description,
#         "vector": content_vector
#     }
#     try:
#         container.create_item(body=book)
#         print(f"Book '{title}' added successfully.")
#     except exceptions.CosmosHttpResponseError as e:
#         print(f"Failed to add book '{title}': {e.message}")
        
# with open('./test/book_details.csv', mode='r', encoding='utf-8') as file:
#     csv_reader = csv.DictReader(file)

#     n=0
#     for row in csv_reader:
#         book_id = str(random.randint(999999999, 9999999999))
#         title = row['title']
#         author = "Boba Fett"
#         isbn = str(random.randint(999999999, 9999999999))
#         description = row['description']
#         embedded = openai_embeddings.embed_query(title + " " + description)
        
#         add_book(container, book_id, isbn, title, description, author, embedded)
        
#         n += 1
#         if n % 10 == 0:
#             break