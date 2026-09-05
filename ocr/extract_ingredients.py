from .extract_text import extract_text
import re


def extract_ingredients(text):

    lower_text = text.lower()


    # ==========================================
    # Find Ingredients Section
    # ==========================================

    ingredient_words = [
        "ingredients",
        "ingredents",
        "ingredeents",
        "neredeents",
        "neredeent"
    ]

    start = -1

    for word in ingredient_words:

        position = lower_text.find(word)

        if position != -1:

            start = position
            break


    # Ingredients section not found
    if start == -1:

        return []


    ingredients_text = text[start:]


    # ==========================================
    # Stop at Directions
    # ==========================================

    direction_words = [
        "direction",
        "directions",
        "director"
    ]

    end = -1

    for word in direction_words:

        position = ingredients_text.lower().find(word)

        if position != -1:

            end = position
            break


    if end != -1:

        ingredients_text = ingredients_text[:end]


    # ==========================================
    # Remove "Ingredients"
    # ==========================================

    ingredients_text = re.sub(
        r"(?i)ingredients|ingredents|ingredeents|neredeents|neredeent",
        "",
        ingredients_text
    )


    # ==========================================
    # Remove unwanted OCR characters
    # ==========================================

    ingredients_text = ingredients_text.replace(
        "\n", " "
    )

    ingredients_text = ingredients_text.replace(
        "|", ""
    )

    ingredients_text = ingredients_text.replace(
        ":", ""
    )

    ingredients_text = ingredients_text.replace(
        "=", ""
    )


    # ==========================================
    # Fix common OCR mistakes
    # ==========================================

    corrections = {

        "Sslicylate": "Salicylate",

        "Butyiene": "Butylene",

        "Homosaiate": "Homosalate",

        "Octyidodecanc": "Octyldodecanol",

        "line Oxide": "Zinc Oxide",

        "Ceteary Olivate": "Cetearyl Olivate",

        "4.0-Ethyl": "4-O-Ethyl",

        "Mik Peptide": "Milk Peptide",

        "EthylhexyiGlycerine": "Ethylhexylglycerin",

        "Phenoxy- ethanol": "Phenoxyethanol"
    }


    for wrong, correct in corrections.items():

        ingredients_text = ingredients_text.replace(
            wrong,
            correct
        )


    # ==========================================
    # Clean extra spaces
    # ==========================================

    ingredients_text = re.sub(
        r"\s+",
        " ",
        ingredients_text
    ).strip()


    # ==========================================
    # Convert into ingredient list
    # ==========================================

    ingredients = [

        ingredient.strip(" .|")

        for ingredient in ingredients_text.split(",")

        if ingredient.strip(" .|")

    ]


    return ingredients