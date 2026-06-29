import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ingest_pdf():
    try:
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()
        print(f"PDF carregado: {len(documents)} páginas!")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_documents(documents)
        print(f"Documentos divididos: {len(chunks)} chunks criados!")
        
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        vector_store = PGVector.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
            pre_delete_collection=True
        )

        print("Embeddings armazenados no PostgreeSQL com sucesso!")
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Total de chunks: {len(chunks)}")
    
    except Exception as e:
        print(f"Erro durante a ingestão: {str(e)}")
        exit(1)

if __name__ == "__main__":
    print("Iniciando a ingestão do PDF...")
    ingest_pdf()
    print("Ingestão concluída com sucesso!")