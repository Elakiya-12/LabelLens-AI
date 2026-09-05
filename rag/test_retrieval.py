from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Load the same embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to our existing ChromaDB
vectorstore = Chroma(
    persist_directory="../chroma_db",
    embedding_function=embeddings
)

# Search the knowledge base
query = "What does salicylic acid do?"

results = vectorstore.similarity_search(query, k=1)

print("\nRetrieved Information:\n")
print(results[0].page_content)