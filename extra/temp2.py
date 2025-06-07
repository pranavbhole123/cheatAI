import cv2
from PIL import Image
import pytesseract

# Optional: Set path to tesseract.exe (only needed on Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image
image_path = "your_image.png"
image = cv2.imread(image_path)

# Preprocessing: convert to grayscale and apply thresholding
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Save preprocessed image (optional)
cv2.imwrite("processed_image.png", thresh)

# OCR: extract text
text = pytesseract.image_to_string(thresh, config="--oem 1 --psm 6")

# Print or save result
print("\n--- Extracted Text ---\n")
print(text)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(text)
