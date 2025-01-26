import re

def segment_text(text):
    segments = {
        "Inputs": [],
        "Actions": [],
        "Dependencies": [],
        "Validations": []
    }

    patterns = {
        "Inputs": r"(identify|inputs?|parameters?):? .*",
        "Actions": r"(action|step|perform|execute):? .*",
        "Dependencies": r"(dependency|requires|depends on):? .*",
        "Validations": r"(validate|check|verify|expected results):? .*"
    }

    for line in text.split(". "):  # Split by sentences
        for key, pattern in patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                segments[key].append(line.strip())
                break

    return segments

if __name__ == "__main__":
    # Example usage for testing
    sample_text = "Identify the host. Check for node state. Execute the action. Dependencies include proper permissions."
    segmented_data = segment_text(sample_text)
    print(segmented_data)
