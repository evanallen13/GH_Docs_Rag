import os
import json
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from langchain_openai import OpenAIEmbeddings
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

query_string = "How much does Copilot Enterprise cost?"
query_embedding = openai_embeddings.embed_query(query_string)

k_num = 5
query = f'SELECT TOP {k_num} c.id, c.filename, VectorDistance(c.vector, @embedding) AS SimilarityScore FROM c ORDER BY VectorDistance(c.vector, @embedding)'
parameters = [{"name": "@embedding", "value": query_embedding}]

query_iterable = container.query_items(
    query=query,
    parameters=parameters,
    enable_cross_partition_query=True,
    populate_index_metrics=True,
    populate_query_metrics=True
)

items = list(query_iterable)
for item in items:
    print(json.dumps(item, indent=2))
    
print("Request Units consumed: ",container.client_connection.last_response_headers['x-ms-request-charge'])
