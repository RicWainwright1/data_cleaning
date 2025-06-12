import pandas as pd
import json
import uuid
from data_clean_prompt import DATA_CLEAN_PROMPT



# Load the input CSV file
input_file = "../data/golden_dataset.csv"
df = pd.read_csv(input_file, on_bad_lines='skip', engine="python")

# Model configuration (Consider moving this to a config file or env var)
model_id = "ft:gpt-4.1-nano-2025-04-14:the-insights-family:favourite-sports-cleaners:BYwH5kjs"

# Output file path
batch_file_path = "finetuned_sports_hobbies_cleaning_batch.jsonl"

# Generate batch records
batch_data = []
for _, row in df.iterrows():
    prompt = f"Question: {row['question_text']}\nAnswer: {row['dirty_data']}"
    expected_output = f"{row['expected_output']}"
    custom_id = str(uuid.uuid4())
    record = {
            "messages": [
                {"role": "system", "content": DATA_CLEAN_PROMPT},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": expected_output}
            ]
    }
    batch_data.append(record)
# Write to JSONL file
try:
    with open(batch_file_path, "w", encoding="utf-8") as f:
        for item in batch_data:
            f.write(json.dumps(item) + "\n")

    print(f"Batch file saved to {batch_file_path}")
    print(f"Generated {len(batch_data)} batch records")

except Exception as e:
    print(f"Error writing batch file: {e}")
