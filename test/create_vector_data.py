from src.document_loader import document_loader 
import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.vectorstores.azure_cosmos_db import (
    AzureCosmosDBVectorSearch,
    CosmosDBSimilarityType,
    CosmosDBVectorSearchType,
)
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
EMBEDDING_MODEL = "text-embedding-ada-002"

if __name__ == "__main__":
    print("Loading documents...")
    doc_loader = document_loader()
    documents = doc_loader.load_documents()
    sliced_documents = doc_loader.split_documents(documents) 
    
    openai_embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    conn_string = os.getenv("AZURE_COSMOS_CONNECTION_STRING")

    mongo_client = MongoClient(
        conn_string,
        serverSelectionTimeoutMS=60000,
        connectTimeoutMS=60000,
        socketTimeoutMS=60000
    )
    
    collection = mongo_client["AI"]["VectorStore"]
    try:
        print("Testing connection to Cosmos DB...")
        # List databases to verify connection works
        dbs = mongo_client.list_database_names()
        exit(0)
        print(f"Available databases: {dbs}")
        
        # Check if our database exists
        db_name = "AI"
        collection_name = "VectorStore"
        
        if db_name not in dbs:
            print(f"Database '{db_name}' not found. Creating it...")
            # In MongoDB, databases are created when first referenced
            db = mongo_client[db_name]
            print(f"Created database '{db_name}'")
        else:
            print(f"Database '{db_name}' already exists")
            db = mongo_client[db_name]
        
        # Check if collection exists
        collections = db.list_collection_names()
        print(f"Collections in {db_name}: {collections}")
        
        if collection_name not in collections:
            print(f"Collection '{collection_name}' not found. Creating it...")
            # In MongoDB, collections are created when first referenced
            collection = db.create_collection(collection_name)
            print(f"Created collection '{collection_name}'")
        else:
            print(f"Collection '{collection_name}' already exists")
            collection = db[collection_name]
            
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise
    
    INDEX_NAME = "llama_index"
    
    vectorstore = AzureCosmosDBVectorSearch.from_documents(
        sliced_documents[0:2],
        openai_embeddings,
        collection=collection,
        index_name=INDEX_NAME,
    )
    
    num_lists = 100
    dimensions = 1536
    similarity_algorithm = CosmosDBSimilarityType.COS
    kind = CosmosDBVectorSearchType.VECTOR_IVF
    m = 16
    ef_construction = 64
    ef_search = 40
    score_threshold = 0.1

    vectorstore.create_index(
        num_lists, dimensions, similarity_algorithm, kind, m, ef_construction
    )


    # for doc in sliced_documents[0:10]:
    #     page_content = doc.page_content
    #     metadata = doc.metadata
    #     embedded=get_embedding(page_content)
        
    #     # embed=get_embedding(doc.page_content)
        
    #     # page_content = doc.page_content
    #     # metadata = doc.metadata
        
    #     # print(str(doc))
    #     # print("--------")
    #     # print(embed)
    #     # print("\n \n")