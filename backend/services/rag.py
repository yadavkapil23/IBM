import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Initialize embeddings (runs locally using sentence-transformers for speed/privacy)
# We will use the HF API key later in Phase 4 for the LLM agents.
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize ChromaDB vector store
persist_directory = "./chroma_db"
vector_store = Chroma(
    collection_name="due_diligence_docs",
    embedding_function=embeddings,
    persist_directory=persist_directory
)

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)

def index_document(filename: str, text: str, metadata: dict):
    """
    Splits the parsed text into chunks and stores them in ChromaDB.
    """
    if not text.strip():
        return 0
        
    # Inject filename into metadata
    metadata["source"] = filename
    
    chunks = text_splitter.split_text(text)
    
    # Create metadata for each chunk
    metadatas = [metadata for _ in chunks]
    
    # Add to vector store
    vector_store.add_texts(texts=chunks, metadatas=metadatas)
    
    return len(chunks)

def query_documents(query: str, k: int = 5):
    """
    Retrieves the most relevant chunks for a given query.
    """
    results = vector_store.similarity_search_with_score(query, k=k)
    
    formatted_results = []
    for doc, score in results:
        formatted_results.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "relevance_score": float(score)
        })
        
    return formatted_results
