from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from ocr.extract_text import extract_text
from ocr.extract_ingredients import extract_ingredients

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from groq import Groq
from dotenv import load_dotenv

import os
import re


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

print("GROQ_API_KEY PRESENT:", bool(GROQ_API_KEY))

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is NOT available")

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# RAG SETUP
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "rag",
    "chroma_db"
)

print("======================================")
print("Loading LabelLens RAG...")
print("======================================")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)

print(
    "CHROMA PATH:",
    CHROMA_PATH
)

print(
    "CHROMA RECORDS:",
    db._collection.count()
)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# IMAGE ANALYSIS
# ============================================================
#
# Image
#   ↓
# OCR
#   ↓
# Ingredient Extraction
#   ↓
# JSON response
#
# Groq is NOT called here.
# ============================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    if "image" not in request.files:

        return jsonify({
            "success": False,
            "message": "No image uploaded"
        }), 400

    image = request.files["image"]

    if image.filename == "":

        return jsonify({
            "success": False,
            "message": "No image selected"
        }), 400

    filename = secure_filename(
        image.filename
    )

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    image.save(
        image_path
    )

    try:

        # ====================================================
        # STEP 1: OCR
        # ====================================================

        print("\n======================================")
        print("STEP 1: OCR")
        print("======================================")

        text = extract_text(
            image_path
        )

        print("OCR TEXT:")
        print(text)


        # ====================================================
        # STEP 2: INGREDIENT EXTRACTION
        # ====================================================

        print("\n======================================")
        print("STEP 2: INGREDIENT EXTRACTION")
        print("======================================")

        ingredients = extract_ingredients(
            text
        )

        print("INGREDIENTS:")
        print(ingredients)


        # ====================================================
        # RETURN OCR RESULT
        # ====================================================

        return jsonify({
            "success": True,
            "message":
                "Image analyzed successfully",
            "filename":
                filename,
            "ingredients":
                ingredients,
            "ocr_text":
                text
        })


    except Exception as e:

        print(
            "OCR ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message":
                str(e)
        }), 500


# ============================================================
# FIND INGREDIENT DOCUMENT
# ============================================================

def find_ingredient_document(
    ingredient
):

    ingredient = (
        ingredient
        .lower()
        .strip()
    )

    print(
        "\nSearching RAG for:",
        ingredient
    )

    try:

        # ====================================================
        # EXACT SEARCH
        # ====================================================

        all_data = db.get()

        documents = all_data.get(
            "documents",
            []
        )

        for document in documents:

            lines = document.split(
                "\n"
            )

            for line in lines:

                if line.lower().startswith(
                    "ingredient:"
                ):

                    database_name = (
                        line.split(
                            ":",
                            1
                        )[1]
                        .strip()
                        .lower()
                    )

                    if database_name == ingredient:

                        print(
                            "EXACT MATCH:",
                            database_name
                        )

                        return document


        # ====================================================
        # SEMANTIC SEARCH
        # ====================================================

        print(
            "Trying semantic search..."
        )

        results = db.similarity_search(
            ingredient,
            k=5
        )

        for document in results:

            lines = (
                document.page_content
                .split("\n")
            )

            for line in lines:

                if line.lower().startswith(
                    "ingredient:"
                ):

                    database_name = (
                        line.split(
                            ":",
                            1
                        )[1]
                        .strip()
                        .lower()
                    )

                    if (
                        database_name == ingredient
                        or ingredient in database_name
                        or database_name in ingredient
                    ):

                        print(
                            "SEMANTIC MATCH:",
                            database_name
                        )

                        return (
                            document.page_content
                        )


    except Exception as e:

        print(
            "RAG SEARCH ERROR:",
            e
        )

        return None


    print(
        "NOT FOUND:",
        ingredient
    )

    return None


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are LabelLens AI, an ingredient awareness assistant.

Your job is to explain product ingredients using ONLY the
information provided in the retrieved LabelLens knowledge base.

The ingredient may belong to:

- skincare
- makeup
- cosmetics
- food
- beverages
- personal care
- household products
- or another product category.

Do NOT assume that every ingredient is a skincare ingredient.

Identify the ingredient and explain it according to the
information provided in the knowledge base.

Do NOT invent facts that are not present in the knowledge base.


For the ingredient being analyzed, use exactly this structure:


### 🧪 [Ingredient Name]


**What is it?**

Explain what the ingredient is based on the retrieved
knowledge.


**Why is it added to the product?**

Explain why the ingredient is commonly used and what
purpose it serves, based ONLY on the retrieved knowledge.


**What does it do?**

Explain its main function or effect in simple language.


**Possible benefits:**

- List only benefits supported by the knowledge base.


**Possible concerns:**

Explain only concerns, risks, irritation, sensitivity,
allergy, intolerance, or other cautions that are explicitly
supported by the knowledge base.

If no specific concerns are provided, write:

No specific concerns are mentioned in the current knowledge base.


**Overall:**

Give a simple overall assessment based ONLY on the retrieved
knowledge.

Use one of these indicators when supported by the information:

🟢 Generally suitable

🟡 Depends on usage / concentration / formulation

🔴 May require caution


IMPORTANT RULES:

1. Use ONLY the retrieved LabelLens knowledge.
2. Do NOT use outside knowledge.
3. Do NOT invent benefits.
4. Do NOT invent side effects.
5. Do NOT invent risks.
6. Do NOT invent nutritional information.
7. Do NOT invent medical information.
8. Do NOT automatically treat the ingredient as skincare.
9. Do NOT automatically treat the ingredient as food.
10. Do NOT claim an ingredient is completely safe.
11. Do NOT claim an ingredient is completely harmful.
12. Do not diagnose medical conditions.
13. Keep the explanation simple and consumer-friendly.
14. Do not add unnecessary greetings.
15. Do not say "I'm LabelLens AI".
16. Do not discuss ingredients that were not provided
    in the retrieved knowledge.
17. If the knowledge base does not contain enough
    information, clearly say so.

"""


# ============================================================
# GROQ GENERATION FUNCTION
# ============================================================

def generate_ai_response(
    prompt,
    max_tokens=900
):

    try:

        print(
            "Sending request to Groq..."
        )

        result = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0,

            max_tokens=max_tokens
        )

        answer = (
            result
            .choices[0]
            .message
            .content
            .strip()
        )

        if not answer:

            return (
                "The AI could not generate an explanation. "
                "Please try again."
            )

        print(
            "GROQ RESPONSE RECEIVED"
        )

        return answer


    except Exception as e:

        print(
            "GROQ ERROR:",
            e
        )

        raise e


# ============================================================
# ASK ABOUT INGREDIENT FROM IMAGE
# ============================================================

@app.route(
    "/ask",
    methods=["POST"]
)
def ask():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message":
                "No question received"
        }), 400


    question = (
        data.get(
            "question",
            ""
        )
        .strip()
    )


    ingredients = data.get(
        "ingredients",
        []
    )


    if not question:

        return jsonify({
            "success": False,
            "message":
                "Please enter a question"
        }), 400


    # ========================================================
    # FIND INGREDIENT FROM QUESTION
    # ========================================================

    selected_ingredient = None

    question_lower = (
        question.lower()
    )


    # First check ingredients extracted
    # from uploaded image.

    for ingredient in ingredients:

        ingredient_lower = (
            ingredient.lower().strip()
        )

        if (
            ingredient_lower
            and ingredient_lower in question_lower
        ):

            selected_ingredient = (
                ingredient
            )

            break


    # ========================================================
    # IF USER TYPED ONLY INGREDIENT NAME
    # ========================================================

    if selected_ingredient is None:

        for ingredient in ingredients:

            if (
                question_lower
                == ingredient.lower().strip()
            ):

                selected_ingredient = (
                    ingredient
                )

                break


    # ========================================================
    # OTHERWISE USE QUESTION
    # ========================================================

    if selected_ingredient is None:

        selected_ingredient = question


    print("\n======================================")
    print("STEP 3: RAG ANALYSIS")
    print("======================================")


    print(
        "Ingredient selected:",
        selected_ingredient
    )


    # ========================================================
    # RETRIEVE ONE INGREDIENT
    # ========================================================

    document = find_ingredient_document(
        selected_ingredient
    )


    if document is None:

        return jsonify({
            "success": True,
            "answer":
                "I couldn't find enough information about "
                f"'{selected_ingredient}' in the current "
                "LabelLens knowledge base."
        })


    print(
        "RAG DOCUMENT FOUND"
    )


    # ========================================================
    # GROQ PROMPT
    # ========================================================

    prompt = f"""
USER QUESTION
==================================================

{question}


INGREDIENT BEING ANALYZED
==================================================

{selected_ingredient}


RETRIEVED LABEL LENS KNOWLEDGE
==================================================

{document}


FINAL INSTRUCTION
==================================================

Answer the user's question using ONLY the retrieved
LabelLens knowledge.

Follow the required structure from the system instructions.

Do not add outside information.

"""


    # ========================================================
    # GROQ
    # ========================================================

    try:

        answer = generate_ai_response(
            prompt,
            max_tokens=500
        )

        return jsonify({
            "success": True,
            "answer":
                answer,
            "ingredient":
                selected_ingredient
        })


    except Exception as e:

        print(
            "AI GENERATION ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message":
                f"AI generation error: {e}"
        }), 500


# ============================================================
# MANUAL TEXT ANALYSIS
# ============================================================

@app.route(
    "/analyze-text",
    methods=["POST"]
)
def analyze_text_route():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message":
                "No text received"
        }), 400


    ingredients_text = (
        data.get(
            "ingredients",
            ""
        )
        .strip()
    )


    if not ingredients_text:

        return jsonify({
            "success": False,
            "message":
                "Please enter an ingredient."
        }), 400


    print("\n======================================")
    print("MANUAL TEXT ANALYSIS")
    print("======================================")


    print(
        "INPUT:",
        ingredients_text
    )


    # ========================================================
    # CLEAN TEXT
    # ========================================================

    ingredients_text = (
        ingredients_text
        .replace("\n", " ")
    )

    ingredients_text = re.sub(
        r"\s+",
        " ",
        ingredients_text
    )


    # ========================================================
    # SPLIT INGREDIENTS
    # ========================================================

    ingredients = [

        item.strip(
            " .|"
        )

        for item in ingredients_text.split(",")

        if item.strip(
            " .|"
        )

    ]


    if not ingredients:

        return jsonify({
            "success": False,
            "message":
                "No valid ingredients found."
        }), 400


    print(
        "INGREDIENTS:",
        ingredients
    )


    # ========================================================
    # RETRIEVE INFORMATION
    # ========================================================

    retrieved_documents = []

    found_ingredients = []


    for ingredient in ingredients:

        document = find_ingredient_document(
            ingredient
        )


        if document:

            found_ingredients.append(
                ingredient
            )


            retrieved_documents.append(
                f"""
Ingredient: {ingredient}

Knowledge Base Information:

{document}
"""
            )


    # ========================================================
    # NOTHING FOUND
    # ========================================================

    if not retrieved_documents:

        return jsonify({
            "success": True,
            "analysis":
                "I couldn't find enough information about "
                "the entered ingredient(s) in the current "
                "LabelLens knowledge base."
        })


    # ========================================================
    # CREATE RAG CONTEXT
    # ========================================================

    context = "\n\n".join(
        retrieved_documents
    )


    print(
        "\nFOUND INGREDIENTS:",
        found_ingredients
    )


    print(
        "\nSending retrieved information to Groq..."
    )


    # ========================================================
    # TEXT ANALYSIS PROMPT
    # ========================================================

    prompt = f"""
USER PROVIDED INGREDIENTS
==================================================

{", ".join(ingredients)}


RETRIEVED LABEL LENS KNOWLEDGE
==================================================

{context}


FINAL INSTRUCTION
==================================================

Analyze ONLY the ingredients that have retrieved information.

For each ingredient, follow exactly this structure:

### 🧪 [Ingredient Name]

**What is it?**

Explain using ONLY the retrieved knowledge.

**Why is it added to the product?**

Explain using ONLY the retrieved knowledge.

**What does it do?**

Explain using ONLY the retrieved knowledge.

**Possible benefits:**

- List only benefits explicitly supported by the knowledge base.

**Possible concerns:**

List only concerns explicitly supported by the knowledge base.

If no concerns are provided, write:

No specific concerns are mentioned in the current knowledge base.

**Overall:**

Give a simple assessment based ONLY on the retrieved knowledge.

Use:

🟢 Generally suitable

🟡 Depends on usage / concentration / formulation

🔴 May require caution

Do NOT use outside knowledge.

Do NOT invent information for ingredients that were not found.

Keep the response simple and consumer-friendly.

"""


    # ========================================================
    # GROQ
    # ========================================================

    try:

        analysis = generate_ai_response(
            prompt,
            max_tokens=900
        )

        return jsonify({
            "success": True,
            "analysis":
                analysis,
            "ingredients":
                found_ingredients
        })


    except Exception as e:

        print(
            "TEXT ANALYSIS GROQ ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message":
                f"AI generation error: {e}"
        }), 500


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    print("======================================")
    print("Starting LabelLens AI...")
    print(
        f"Server running on port {port}"
    )
    print("======================================")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )