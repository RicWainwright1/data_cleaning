import pandas as pd
import json
import uuid
from data_clean_prompt import DATA_CLEAN_PROMPT

# Load the input TSV file
input_file = "../data/sports_hobbies_records_to_clean.txt"
df = pd.read_csv(input_file, sep="\t", on_bad_lines='skip', engine="python")

# Model configuration
model_id = "ft:gpt-4o-mini-2024-07-18:the-insights-family:favourite-sports-cleaners:BYwH5kjs"

# Generate batch records
batch_data = []
for _, row in df.iterrows():
    prompt = f"Question: {row['question_text']}\nAnswer: {row['dirty_data']}"
    custom_id = str(uuid.uuid4())
    record = {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": model_id,
            "messages": [
                {"role": "system", "content": DATA_CLEAN_PROMPT},
                {"role": "user", "content": prompt}
            ]
        }
    }
    batch_data.append(record)

# Write to JSONL file
batch_file_path = "sports_hobbies_cleaning_batch.jsonl"
with open(batch_file_path, "w", encoding="utf-8") as f:
    for item in batch_data:
        f.write(json.dumps(item) + "\n")

print(f"Batch file saved to {batch_file_path}")
print(f"Generated {len(batch_data)} batch records")