from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import json
import os
from openai import AzureOpenAI
import random
import uuid
import csv
import os
from dotenv import load_dotenv
load_dotenv()

EMBEDDING_MODEL="text-embedding-ada-002"
DB_NAME = 'MyDatabase'
CONTAINER_NAME = 'bookstore'
COSMOS_DB_ACCOUNT = os.getenv("COSMOS_DB_ACCOUNT")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

with open("./test/policies/indexing_policy.json", "r") as file: indexing_policy = json.load(file)
with open("./test/policies/vector_embedding_policy.json", "r") as file: vector_embedding_policy = json.load(file)

aad_credentials = DefaultAzureCredential()
db=CosmosClient("https://test43442343.documents.azure.com:443/", aad_credentials).get_database_client(DB_NAME)

try:
    container = db.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key=PartitionKey(path='/id'),
        indexing_policy=indexing_policy,
        vector_embedding_policy=vector_embedding_policy
    )
    print('Container with id \'{0}\' created'.format(CONTAINER_NAME))

except exceptions.CosmosHttpResponseError:
    print('Container with id \'{0}\' already exists'.format(CONTAINER_NAME))
    
def add_book(container, book_id, isbn, title, description, author, content_vector):
    book = {
        "id": book_id,
        "title": title,
        "isbn": isbn,
        "author": author,
        "description": description,
        "contentVector": content_vector
    }
    try:
        container.create_item(body=book)
        print(f"Book '{title}' added successfully.")
    except exceptions.CosmosHttpResponseError as e:
        print(f"Failed to add book '{title}': {e.message}")


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
) 
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    azure_ad_token_provider=token_provider,
    azure_deployment="ada-002",
    api_version="2024-10-21"
)

with open('book_details.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)

    n=0
    for row in csv_reader:
        book_id = str(uuid.uuid4())
        title = row['title']
        author = "Boba Fett"
        isbn = str(random.randint(999999999, 9999999999))
        description = row['description']
        embedded = query_embedding = client.embeddings.create(model=EMBEDDING_MODEL, input=(title + " " + description)).data[0].embedding  # Access the embedding vector
        
        add_book(container, book_id, isbn, title, description, author, embedded)
        
        n+=1
        if n % 100 == 0:
            break