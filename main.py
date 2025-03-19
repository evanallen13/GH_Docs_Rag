from src.git_helper import git_helper
from src.document_loader import document_loader # type: ignore

if __name__ == "__main__":
    git_helper() # clone or update the GitHub repository
    
    document_loader = document_loader()
    documents = document_loader.load_documents()
    sliced_documents = document_loader.split_documents(documents) 
    
    print(len(documents))
