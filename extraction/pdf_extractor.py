import os
import re
from pdfminer.high_level import extract_text


RAW_DATA_DIR = "/Users/nandish.chokshi/Downloads/NLP_Based_KBA/data/raw"
PROCESSED_DATA_DIR = "/Users/nandish.chokshi/Downloads/NLP_Based_KBA/data/processed"

def extract_text_from_pdf(file_path):
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None

def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    return text.strip()

def process_raw_pdfs():
    for file_name in os.listdir(RAW_DATA_DIR):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(RAW_DATA_DIR, file_name)
            print(f"Processing file: {file_name}")
            raw_text = extract_text_from_pdf(file_path)
            if raw_text:
                cleaned_text = clean_text(raw_text)
                output_path = os.path.join(PROCESSED_DATA_DIR, f"{os.path.splitext(file_name)[0]}.txt")
                with open(output_path, "w") as f:
                    f.write(cleaned_text)
                print(f"Processed and saved: {output_path}")

if __name__ == "__main__":
    if not os.path.exists(PROCESSED_DATA_DIR):
        os.makedirs(PROCESSED_DATA_DIR)
    process_raw_pdfs()
