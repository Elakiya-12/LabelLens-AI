from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import ollama
import re
import os


# --------------------------------------------------
# 1. Load embedding model
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 2. Load ChromaDB
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)

print("CHROMA PATH:", CHROMA_PATH)
print("CHROMA RECORDS:", db._collection.count())


# --------------------------------------------------
# 3. Analyze ingredients
# --------------------------------------------------

def analyze_ingredients(ingredients_text, skin_type="Not specified"):

    # --------------------------------------------------
    # Clean input
    # --------------------------------------------------

    ingredients_text = ingredients_text.replace("\n", " ")
    ingredients_text = re.sub(r"\s+", " ", ingredients_text)

    # Split ingredients
    ingredients = [
        item.strip(" .|")
        for item in ingredients_text.split(",")
        if item.strip(" .|")
    ]

    if not ingredients:
        return "I couldn't find any ingredients to analyze."


    # --------------------------------------------------
    # 4. Get documents from ChromaDB
    # --------------------------------------------------

    retrieved = []
    found_ingredients = []

    try:

        all_data = db.get()

        all_documents = all_data.get(
            "documents",
            []
        )

    except Exception as e:

        return f"ChromaDB error: {e}"


    # --------------------------------------------------
    # 5. Search for each ingredient
    # --------------------------------------------------

    for ingredient in ingredients:

        print(f"Searching: {ingredient}")

        found_document = None

        search_name = ingredient.lower().strip()


        # --------------------------------------------------
        # A. Exact ingredient match
        # --------------------------------------------------

        for document in all_documents:

            lines = document.split("\n")

            for line in lines:

                if line.lower().startswith("ingredient:"):

                    database_name = line.split(
                        ":",
                        1
                    )[1].strip().lower()

                    if database_name == search_name:

                        found_document = document

                        break

            if found_document:
                break


        # --------------------------------------------------
        # B. Semantic search if exact match not found
        # --------------------------------------------------

        if found_document is None:

            try:

                results = db.similarity_search(
                    ingredient,
                    k=5
                )

                for document in results:

                    lines = document.page_content.split("\n")

                    for line in lines:

                        if line.lower().startswith("ingredient:"):

                            database_name = line.split(
                                ":",
                                1
                            )[1].strip().lower()

                            if (
                                database_name == search_name
                                or search_name in database_name
                                or database_name in search_name
                            ):

                                found_document = (
                                    document.page_content
                                )

                                break

                    if found_document:
                        break

            except Exception as e:

                print(
                    "Semantic search error:",
                    e
                )


        # --------------------------------------------------
        # C. Store result
        # --------------------------------------------------

        if found_document:

            print(
                f"FOUND: {ingredient}"
            )

            found_ingredients.append(
                ingredient
            )

            retrieved.append(
                f"""
Ingredient: {ingredient}

Knowledge Base Information:
{found_document}
"""
            )

        else:

            print(
                f"NOT FOUND: {ingredient}"
            )


    # --------------------------------------------------
    # 6. Nothing found
    # --------------------------------------------------

    if not retrieved:

        return (
            "I couldn't find information about these "
            "ingredients in the LabelLens knowledge base."
        )


    # --------------------------------------------------
    # 7. Create RAG context
    # --------------------------------------------------

    context = "\n\n".join(
        retrieved
    )


    # --------------------------------------------------
    # 8. Create skin-type instruction
    # --------------------------------------------------

    if skin_type == "Not specified":

        skin_instruction = """
The user has not specified a skin type.

Do NOT make skin-type-specific recommendations.

Only analyze the ingredients using the retrieved
knowledge base information.
"""

    else:

        skin_instruction = f"""
The user's skin type is: {skin_type}

After explaining the ingredients, give a simple
skin-type suitability observation.

IMPORTANT:

- Use ONLY information supported by the retrieved
  knowledge base.
- Do not invent skin reactions.
- Do not claim an ingredient is safe or harmful
  for this skin type unless the knowledge base
  supports it.
- If the knowledge base does not contain enough
  information to determine suitability for this
  skin type, clearly say that there is not enough
  information.
"""


    # --------------------------------------------------
    # 9. Prompt Ollama
    # --------------------------------------------------

    prompt = f"""
You are LabelLens AI, an ingredient awareness assistant.

Your job is to explain product ingredients using ONLY the information
provided in the retrieved knowledge base.

Do not invent facts that are not present in the knowledge base.

Product ingredients:
{", ".join(ingredients)}

User's skin type:
{skin_type}

Retrieved information from the LabelLens knowledge base:

{context}

{skin_instruction}

For every ingredient that was found in the knowledge base, explain it
using EXACTLY this structure:

### 🧪 [Ingredient Name]

**What is it?**

Explain what the ingredient is based on the knowledge provided.

**Why is it added to the product?**

Explain why it is commonly used and what purpose it serves.

Use information from fields such as:

- Common uses
- Function
- Typical product categories
- Purpose
- Similar information available in the knowledge base

**What does it do?**

Explain its main function or effect using only the retrieved information.

**Possible benefits:**

- List the benefits mentioned in the knowledge base.
- Keep the explanation simple and easy to understand.

**Possible concerns:**

Explain the potential concerns mentioned in the knowledge base.

Mention conditions such as:

- frequent use
- higher concentrations
- sensitivity
- irritation

ONLY when these are supported by the retrieved information.

**👤 For your skin type — {skin_type}:**

Explain whether the ingredient may be suitable for the selected skin type
using ONLY the retrieved information.

If the knowledge base does not provide enough information about the
selected skin type, say:

"Not enough information in the current knowledge base to determine
skin-type suitability."

**Overall:**

Give a simple overall assessment based only on the retrieved information.

Use one of these indicators when supported by the information:

🟢 Generally suitable

🟡 Depends on usage / concentration / formulation

🔴 May require caution

Choose an indicator only when the retrieved information supports it.

IMPORTANT RULES:

1. Use ONLY the retrieved knowledge base as your factual source.
2. Do NOT add outside facts.
3. Do NOT invent benefits.
4. Do NOT invent side effects.
5. Do NOT invent risks.
6. Do NOT invent skin-type reactions.
7. Do NOT make medical diagnoses.
8. Do NOT claim an ingredient is completely safe or completely harmful.
9. If the knowledge base does not contain enough information, clearly say so.
10. Keep the explanation simple and consumer-friendly.
11. Do not repeat unnecessary introductions.
12. Do not say "I'm LabelLens AI".
13. Do not use unnecessary greetings.
14. Keep the answer focused on the ingredients.
15. Separate each ingredient clearly.
"""


    # --------------------------------------------------
    # 10. Generate response using Ollama
    # --------------------------------------------------

    try:

        result = ollama.generate(
            model="llama3.2:3b",
            prompt=prompt,
            options={
                "temperature": 0,
                "num_predict": 1200
            }
        )

        response = result.get(
            "response",
            ""
        ).strip()

    except Exception as e:

        return (
            f"AI generation error: {e}"
        )


    # --------------------------------------------------
    # 11. Check response
    # --------------------------------------------------

    if not response:

        return (
            "The AI could not generate a response. "
            "Please try again."
        )


    return response