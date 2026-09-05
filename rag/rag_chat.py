from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM


# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to ChromaDB
vectorstore = Chroma(
    persist_directory="../chroma_db",
    embedding_function=embeddings
)

# Connect to Ollama
llm = OllamaLLM(model="qwen3:4b")


# Ask the user
query = input("Ask about an ingredient: ")


# Retrieve relevant documents
results = vectorstore.similarity_search(query, k=2)

context = "\n\n".join(
    document.page_content for document in results
)


# Create prompt
prompt = f"""
You are LabelLens AI, a product ingredient analysis assistant.

Use ONLY the information provided in the context.

Context:
{context}

User question:
{query}

Give a simple and clear answer.
"""


# Generate answer using Qwen
print("\nGenerating answer...\n")

answer = llm.invoke(prompt)

print("LabelLens AI:")
print(answer)