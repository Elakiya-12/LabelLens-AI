from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import os

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

def extract_text(image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")

    width, height = image.size
    image = image.resize((width * 3, height * 3))

    image = ImageEnhance.Contrast(image).enhance(2)
    image = image.filter(ImageFilter.SHARPEN)

    text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )

    return text