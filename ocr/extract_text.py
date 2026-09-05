from PIL import Image, ImageEnhance, ImageFilter
import pytesseract


# Tesseract location on Windows
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_path):

    # Open image
    image = Image.open(image_path)

    # Convert to RGB
    image = image.convert("RGB")

    # Resize image
    width, height = image.size

    image = image.resize(
        (width * 3, height * 3)
    )

    # Improve contrast
    image = ImageEnhance.Contrast(image).enhance(2)

    # Sharpen image
    image = image.filter(
        ImageFilter.SHARPEN
    )

    # Perform OCR
    text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )

    return text