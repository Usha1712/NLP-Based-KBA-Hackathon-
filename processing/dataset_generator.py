import os
import json
from text_segment import segment_text

PROCESSED_DATA_DIR = "/Users/nandish.chokshi/Downloads/NLP_Based_KBA/data/processed"
OUTPUT_FILE = "/Users/nandish.chokshi/Downloads/NLP_Based_KBA/data/processed/structured_dataset.json"

def save_structured_data(input_dir, output_file):
    dataset = []

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".txt"):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, "r") as f:
                text = f.read()

            structured_data = segment_text(text)

            dataset.append({
                "file_name": file_name,
                "structured_data": structured_data
            })

    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Structured dataset saved at: {output_file}")

if __name__ == "__main__":
    save_structured_data(PROCESSED_DATA_DIR, OUTPUT_FILE)
