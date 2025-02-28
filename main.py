import cv2
import pytesseract
import time

def extract_text(image_path):
    start = time.time()
    image = cv2.imread(image_path)
    text = pytesseract.image_to_string(image)
    end = time.time()
    print(f"Time taken to extract text: {end - start} seconds")
    return text


print(extract_text("60c4199364474569561cba359d486e6c69ae8cba_2_451x525.jpeg"))
