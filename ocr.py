from PIL import Image
import pytesseract


def ocr(imgPath: str):
    # Correct the Tesseract executable path
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Samim\tesseract.exe"

    # Perform OCR
    text = pytesseract.image_to_string(Image.open(imgPath))

    return text


if __name__ == "__main__":
    extracted_text = ocr("image.png")
    print(extracted_text)  # Display the OCR result
