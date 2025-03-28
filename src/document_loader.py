from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os

class document_loader: 
    
    # def load_documents(self, DATA_PATH="data"):
        
    #     documents = []
    #     for file in os.listdir(DATA_PATH):
    #         if file.endswith(".md"):
    #             try:
    #                 loader = TextLoader(os.path.join(DATA_PATH, file), encoding='utf-8')
    #                 documents.extend(loader.load())
    #             except Exception as e:
    #                 print(f"Error loading {file}: {str(e)}")

    #     return documents
    def load_documents(self, DATA_PATH="data"):
        documents = []
        
        # Use os.walk to iterate over all directories and subdirectories
        for root, dirs, files in os.walk(DATA_PATH):
            for file in files:
                if file.endswith(".md"):
                    try:
                        file_path = os.path.join(root, file)
                        loader = TextLoader(file_path, encoding='utf-8')
                        documents.extend(loader.load())
                    except Exception as e:
                        print(f"Error loading {file}: {str(e)}")

        return documents

    def split_documents(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)