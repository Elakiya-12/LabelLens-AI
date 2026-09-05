from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import shutil


# ============================================================
# 1. DATA PATH
# ============================================================

data_path = "../data"


if not os.path.exists(data_path):
    print("Data folder not found:", os.path.abspath(data_path))
    exit()


# ============================================================
# 2. LOAD TXT FILES
# ============================================================

loader = DirectoryLoader(
    data_path,
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

documents = loader.load()

print(f"Loaded {len(documents)} documents")


if len(documents) == 0:
    print("No TXT files found.")
    exit()


# ============================================================
# 3. SPLIT DOCUMENTS
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")


# ============================================================
# 4. EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# 5. REMOVE OLD CHROMA DATABASE
# ============================================================

if os.path.exists("chroma_db"):
    print("Removing old ChromaDB...")
    shutil.rmtree("chroma_db")


# ============================================================
# 6. CREATE NEW CHROMADB
# ============================================================

print("Creating ChromaDB...")

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)


# ============================================================
# 7. RESULT
# ============================================================

print()
print("========================================")
print("Documents successfully stored!")
print("========================================")
print("Documents:", len(documents))
print("Chunks:", len(chunks))
print("ChromaDB records:", db._collection.count())
print("========================================")