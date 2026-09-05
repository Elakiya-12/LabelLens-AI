from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import ollama
import re


# ==================================================
# 1. Load embedding model
# ==================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==================================================
# 2. Load ChromaDB
# ==================================================

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


# ==================================================
# 3. Read extracted ingredients
# ==================================================

with open("../ocr/ingredients.txt", "r", encoding="utf-8") as f:
    ingredients_text = f.read()


# ==================================================
# 4. Clean ingredients
# ==================================================

ingredients_text = ingredients_text.replace("\n", " ")
ingredients_text = re.sub(r"\s+", " ", ingredients_text)

ingredients = [
    item.strip(" .|")
    for item in ingredients_text.split(",")
    if item.strip(" .|")
]


print("\nAnalyzing product...")
print(f"Ingredients found: {len(ingredients)}")


# ==================================================
# 5. Retrieve information from ChromaDB
# ==================================================

retrieved = []
seen_sources = set()

for ingredient in ingredients:

    print(f"Searching: {ingredient}")

    results = db.similarity_search(
        ingredient,
        k=1
    )

    if results:

        document = results[0]

        source = document.metadata.get("source", "")

        if source not in seen_sources:

            seen_sources.add(source)

            retrieved.append(
                f"""
Ingredient: {ingredient}

{document.page_content}
"""
            )


# ==================================================
# 6. Check retrieval
# ==================================================

if not retrieved:

    print("\nNo relevant information found in ChromaDB.")
    exit()


context = "\n".join(retrieved)

print("\nRetrieved ingredients:", len(retrieved))
print("Retrieved context length:", len(context))


# ==================================================
# 7. Short prompt
# ==================================================

prompt = f"""
You are LabelLens AI.

Analyze these ingredients using ONLY the information provided.

Ingredients:
{", ".join(ingredients)}

Knowledge:
{context}

Give a concise answer:

1. Overall Summary
2. Beneficial Ingredients
3. Ingredients to Be Aware Of
4. Main Purpose
5. Final Assessment

Only discuss ingredients present in the knowledge.
Do not invent information.
"""


# ==================================================
# 8. Generate using Ollama
# ==================================================

print("\nGenerating analysis...\n")

result = ollama.generate(
    model="llama3.2:3b",
    prompt=prompt,
    options={
        "temperature": 0,
        "num_predict": 400
    }
)


# ==================================================
# 9. Get response
# ==================================================

response = result.get("response", "").strip()


# ==================================================
# 10. Display
# ==================================================

print("========== LabelLens AI ==========\n")

if response:
    print(response)
else:
    print("The AI did not generate a response.")
    print("\nDebug information:")
    print("Done reason:", result.get("done_reason"))
    print("Thinking:", result.get("thinking", "")[:500])