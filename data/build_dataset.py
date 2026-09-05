import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

OUTPUT = DATA_DIR / "labellens_ingredients.csv"


# ---------------------------------------------------------
# Existing ingredient knowledge
# ---------------------------------------------------------

records = [

    # =========================
    # SKINCARE / COSMETICS
    # =========================

    {
        "ingredient": "Glycerin",
        "category": "Skincare",
        "what_it_is": "A humectant commonly used in skincare and cosmetics.",
        "function": "Humectant and skin conditioning agent.",
        "benefits": "Helps attract and retain water in the outer layer of the skin.",
        "concerns": "Generally well tolerated when used appropriately, although individual irritation is possible.",
        "source": "CosIng / cosmetic ingredient references"
    },

    {
        "ingredient": "Niacinamide",
        "category": "Skincare",
        "what_it_is": "A form of vitamin B3 used in cosmetic formulations.",
        "function": "Skin conditioning and cosmetic active.",
        "benefits": "Commonly used in products designed to support the appearance and condition of skin.",
        "concerns": "Some people may experience irritation, especially with highly concentrated formulations.",
        "source": "CosIng / cosmetic ingredient references"
    },

    {
        "ingredient": "Salicylic Acid",
        "category": "Skincare",
        "what_it_is": "A beta-hydroxy acid used in skincare and topical products.",
        "function": "Exfoliating and keratolytic ingredient.",
        "benefits": "Helps remove dead skin cells and is commonly used in products for blemish-prone skin.",
        "concerns": "May cause dryness or irritation, particularly when overused.",
        "source": "CosIng / cosmetic ingredient references"
    },

    {
        "ingredient": "Hyaluronic Acid",
        "category": "Skincare",
        "what_it_is": "A water-binding substance used in cosmetic formulations.",
        "function": "Humectant and skin conditioning ingredient.",
        "benefits": "Helps improve the hydrated appearance of skin.",
        "concerns": "Usually well tolerated, but any cosmetic ingredient may cause individual sensitivity.",
        "source": "CosIng / cosmetic ingredient references"
    },

    {
        "ingredient": "Cyclopentasiloxane",
        "category": "Cosmetics",
        "what_it_is": "A volatile silicone commonly used in cosmetic formulations.",
        "function": "Skin conditioning, hair conditioning and formulation aid.",
        "benefits": "Provides a smooth, silky sensory feel and helps products spread easily.",
        "concerns": "Safety and environmental considerations depend on concentration, product type and regulatory jurisdiction.",
        "source": "Cosmetic ingredient references"
    },

    {
        "ingredient": "Dimethicone",
        "category": "Skincare",
        "what_it_is": "A silicone polymer widely used in cosmetics.",
        "function": "Skin conditioning and emollient.",
        "benefits": "Helps provide a smooth skin feel and can reduce moisture loss from the skin surface.",
        "concerns": "Some users may dislike its texture; individual sensitivity is possible.",
        "source": "Cosmetic ingredient references"
    },

    {
        "ingredient": "Phenoxyethanol",
        "category": "Cosmetics",
        "what_it_is": "A preservative used in many cosmetic formulations.",
        "function": "Preservative.",
        "benefits": "Helps protect cosmetic products from microbial contamination.",
        "concerns": "Can cause irritation or sensitization in some individuals.",
        "source": "CosIng / cosmetic ingredient references"
    },

    {
        "ingredient": "Tocopherol",
        "category": "Skincare",
        "what_it_is": "Vitamin E used in cosmetic formulations.",
        "function": "Antioxidant and skin conditioning ingredient.",
        "benefits": "Used to help protect formulations from oxidation and condition the skin.",
        "concerns": "Individual sensitivity is possible.",
        "source": "CosIng / cosmetic ingredient references"
    },

    {
        "ingredient": "Kojic Acid",
        "category": "Skincare",
        "what_it_is": "An ingredient used in cosmetic products targeting the appearance of uneven pigmentation.",
        "function": "Skin conditioning and cosmetic active.",
        "benefits": "Commonly used in products intended to improve the appearance of uneven skin tone.",
        "concerns": "Can cause irritation or sensitivity in some users.",
        "source": "Cosmetic ingredient references"
    },

    {
        "ingredient": "Avobenzone",
        "category": "Sun Care",
        "what_it_is": "An organic UV filter used in sunscreen formulations.",
        "function": "Ultraviolet absorber.",
        "benefits": "Used to help protect skin from UVA radiation in sunscreen products.",
        "concerns": "May cause irritation in sensitive individuals.",
        "source": "CosIng / cosmetic ingredient references"
    },

    # =========================
    # FOOD
    # =========================

    {
        "ingredient": "Citric Acid",
        "category": "Food",
        "what_it_is": "An organic acid naturally present in many fruits and widely used in food.",
        "function": "Acidulant and formulation aid.",
        "benefits": "Provides acidity and contributes to flavor and preservation of some foods.",
        "concerns": "High-acidity foods can contribute to dental erosion or irritation in susceptible people.",
        "source": "FDA Substances Added to Food"
    },

    {
        "ingredient": "Acesulfame Potassium",
        "category": "Food",
        "what_it_is": "A high-intensity sweetener used in food and beverages.",
        "function": "Non-nutritive sweetener.",
        "benefits": "Provides sweetness with very little energy.",
        "concerns": "Consumption should remain within applicable safety guidance.",
        "source": "FDA Substances Added to Food"
    },

    {
        "ingredient": "Gum Arabic",
        "category": "Food",
        "what_it_is": "A gum obtained from Acacia species.",
        "function": "Emulsifier, stabilizer, thickener and texturizer.",
        "benefits": "Helps improve texture and stability in food products.",
        "concerns": "Some individuals may experience digestive discomfort or sensitivity.",
        "source": "FDA Substances Added to Food"
    },

    {
        "ingredient": "Sodium Benzoate",
        "category": "Food",
        "what_it_is": "A sodium salt of benzoic acid used as a food preservative.",
        "function": "Preservative.",
        "benefits": "Helps inhibit microbial growth in appropriate food formulations.",
        "concerns": "Some individuals may be sensitive to preservatives.",
        "source": "FDA Substances Added to Food"
    },

    {
        "ingredient": "Potassium Sorbate",
        "category": "Food",
        "what_it_is": "A potassium salt of sorbic acid used as a preservative.",
        "function": "Preservative.",
        "benefits": "Helps control mold and yeast growth in food products.",
        "concerns": "Some individuals may experience sensitivity or irritation.",
        "source": "FDA Substances Added to Food"
    },

]


df = pd.DataFrame(records)

df = df.drop_duplicates(
    subset=["ingredient"],
    keep="first"
)

df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8"
)

print(f"Created: {OUTPUT}")
print(f"Records: {len(df)}")