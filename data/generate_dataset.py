import os
import json

OUTPUT_DIR = "ingredients"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# SKINCARE + MAKEUP INGREDIENTS
# ============================================================

cosmetic_ingredients = [
    "Cyclopentasiloxane",
    "Dimethicone",
    "Cyclomethicone",
    "Trimethylsiloxysilicate",
    "Phenyl Trimethicone",
    "Amodimethicone",
    "Methicone",
    "Silica",
    "Talc",
    "Mica",
    "Kaolin",
    "Bentonite",
    "Zinc Oxide",
    "Titanium Dioxide",
    "Iron Oxides",
    "Ultramarines",
    "Chromium Oxide Greens",
    "Bismuth Oxychloride",
    "Carmine",
    "Synthetic Fluorphlogopite",

    "Glycerin",
    "Hyaluronic Acid",
    "Sodium Hyaluronate",
    "Hydrolyzed Hyaluronic Acid",
    "Niacinamide",
    "Panthenol",
    "Allantoin",
    "Betaine",
    "Sorbitol",
    "Propylene Glycol",
    "Butylene Glycol",
    "Pentylene Glycol",
    "Dipropylene Glycol",
    "1,2-Hexanediol",
    "Caprylyl Glycol",
    "Saccharide Isomerate",
    "Trehalose",
    "Urea",
    "Sodium PCA",

    "Salicylic Acid",
    "Glycolic Acid",
    "Lactic Acid",
    "Mandelic Acid",
    "Azelaic Acid",
    "Kojic Acid",
    "Retinol",
    "Retinal",
    "Retinyl Palmitate",
    "Ascorbic Acid",
    "Sodium Ascorbyl Phosphate",
    "Magnesium Ascorbyl Phosphate",
    "Tocopherol",
    "Tocopheryl Acetate",

    "Ceramide NP",
    "Ceramide AP",
    "Ceramide EOP",
    "Cholesterol",
    "Phytosphingosine",
    "Squalane",
    "Squalene",
    "Shea Butter",
    "Cocoa Butter",
    "Jojoba Oil",
    "Argan Oil",
    "Rosehip Oil",
    "Sunflower Oil",
    "Sweet Almond Oil",
    "Coconut Oil",
    "Olive Oil",

    "Caffeine",
    "Green Tea Extract",
    "Centella Asiatica Extract",
    "Aloe Vera",
    "Chamomile Extract",
    "Licorice Root Extract",
    "Turmeric Extract",
    "Rosemary Extract",
    "Witch Hazel",
    "Tea Tree Oil",

    "Phenoxyethanol",
    "Ethylhexylglycerin",
    "Sodium Benzoate",
    "Potassium Sorbate",
    "Benzyl Alcohol",
    "Dehydroacetic Acid",
    "Sorbic Acid",
    "Benzoic Acid",

    "Fragrance",
    "Parfum",
    "Limonene",
    "Linalool",
    "Citronellol",
    "Geraniol",
    "Eugenol",
    "Hexyl Cinnamal",

    "Avobenzone",
    "Octocrylene",
    "Octinoxate",
    "Octisalate",
    "Homosalate",
    "Uvinul A Plus",
    "Tinosorb S",
    "Tinosorb M",

    "Cetearyl Alcohol",
    "Cetyl Alcohol",
    "Stearyl Alcohol",
    "Behenyl Alcohol",
    "Glyceryl Stearate",
    "PEG-100 Stearate",
    "Polysorbate 20",
    "Polysorbate 60",
    "Polysorbate 80",
    "Lecithin",
    "Sorbitan Olivate",

    "Carbomer",
    "Xanthan Gum",
    "Hydroxyethylcellulose",
    "Cellulose Gum",
    "Sodium Carbomer",
    "Acrylates Copolymer",

    "Sodium Hydroxide",
    "Citric Acid",
    "Triethanolamine",
    "Tromethamine",
    "Disodium EDTA",
    "Tetrasodium EDTA",
]


# ============================================================
# FOOD INGREDIENTS
# ============================================================

food_ingredients = [
    "Sugar",
    "Sucrose",
    "Glucose",
    "Fructose",
    "Maltose",
    "Lactose",
    "Dextrose",
    "Maltodextrin",
    "Corn Syrup",
    "High Fructose Corn Syrup",
    "Brown Sugar",
    "Cane Sugar",
    "Coconut Sugar",
    "Maple Syrup",
    "Honey",
    "Molasses",

    "Sodium Chloride",
    "Potassium Chloride",
    "Calcium Chloride",
    "Monosodium Glutamate",
    "Disodium Inosinate",
    "Disodium Guanylate",
    "Yeast Extract",

    "Citric Acid",
    "Malic Acid",
    "Lactic Acid",
    "Acetic Acid",
    "Tartaric Acid",
    "Phosphoric Acid",
    "Ascorbic Acid",

    "Sodium Benzoate",
    "Potassium Sorbate",
    "Calcium Propionate",
    "Sodium Propionate",
    "Sodium Nitrite",
    "Sodium Nitrate",
    "Sulfur Dioxide",
    "Sodium Metabisulfite",

    "Baking Soda",
    "Sodium Bicarbonate",
    "Ammonium Bicarbonate",
    "Potassium Bicarbonate",

    "Xanthan Gum",
    "Guar Gum",
    "Locust Bean Gum",
    "Gellan Gum",
    "Carrageenan",
    "Pectin",
    "Agar",
    "Gelatin",
    "Modified Starch",
    "Corn Starch",
    "Potato Starch",
    "Tapioca Starch",

    "Lecithin",
    "Soy Lecithin",
    "Mono and Diglycerides",
    "Polysorbate 80",
    "Polysorbate 60",
    "Sodium Stearoyl Lactylate",

    "Aspartame",
    "Sucralose",
    "Saccharin",
    "Acesulfame Potassium",
    "Stevia",
    "Steviol Glycosides",
    "Erythritol",
    "Xylitol",
    "Sorbitol",

    "Annatto",
    "Paprika Extract",
    "Caramel Color",
    "Beta Carotene",
    "Beetroot Red",
    "Curcumin",
    "Titanium Dioxide",

    "Vitamin C",
    "Vitamin D",
    "Vitamin E",
    "Vitamin B12",
    "Vitamin B6",
    "Folic Acid",
    "Niacin",
    "Riboflavin",
    "Thiamine",
    "Calcium",
    "Iron",
    "Zinc",
    "Magnesium",
    "Potassium",
]


# ============================================================
# KNOWLEDGE GENERATION
# ============================================================

def cosmetic_template(name):
    return f"""
Ingredient: {name}

Category: Cosmetic / Skincare / Makeup

What it is:
{name} is an ingredient used in cosmetic and personal-care formulations.

Common function:
It may be used to provide a specific formulation, skin-care, cleansing,
texture, preservation, moisturizing, coloring, or product-performance role,
depending on the formulation.

Benefits / purpose:
The purpose of {name} depends on the type and concentration of the product.
It can contribute to the formulation's intended properties.

Possible concerns:
Individual reactions can vary. People with known sensitivities should
check the complete ingredient list and product instructions.

LabelLens assessment:
Generally used in cosmetic formulations. The overall suitability depends
on the complete formulation, concentration, and individual sensitivity.

Important:
This information is educational and should not be treated as medical advice.
"""


def food_template(name):
    return f"""
Ingredient: {name}

Category: Food / Food Ingredient

What it is:
{name} is an ingredient or food-related substance that may be used in
food products.

Common function:
Its function can include sweetening, preservation, flavoring, coloring,
thickening, stabilizing, acidity control, texture improvement, or nutritional
fortification depending on the product.

Benefits / purpose:
Its purpose depends on how it is used in the food and the amount consumed.

Possible concerns:
Individual tolerance varies. People with allergies, intolerances, dietary
restrictions, or specific health conditions should check the complete label.

LabelLens assessment:
Generally used in food products. The overall nutritional quality of a
product depends on the complete ingredient list, serving size, and nutrition
information.

Important:
This information is educational and should not be treated as medical advice.
"""


# ============================================================
# CREATE FILES
# ============================================================

cosmetic_file = os.path.join(OUTPUT_DIR, "cosmetic_ingredients.txt")
food_file = os.path.join(OUTPUT_DIR, "food_ingredients.txt")


with open(cosmetic_file, "w", encoding="utf-8") as f:

    for ingredient in cosmetic_ingredients:
        f.write(cosmetic_template(ingredient))
        f.write("\n" + "=" * 80 + "\n")


with open(food_file, "w", encoding="utf-8") as f:

    for ingredient in food_ingredients:
        f.write(food_template(ingredient))
        f.write("\n" + "=" * 80 + "\n")


print("Dataset files created successfully!")
print("Cosmetic ingredients:", len(cosmetic_ingredients))
print("Food ingredients:", len(food_ingredients))
print("Total records:", len(cosmetic_ingredients) + len(food_ingredients))