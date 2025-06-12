import openai
import pandas as pd
import json
import os


# Authenticate
openai.api_key = os.getenv("OPENAI_API_KEY")

# Provide your batch_id
batch_id = "batch_684752c7b59881908699f6d9496d29a3"

# === Step 3: Check batch status ===
batch_info = openai.batches.retrieve(batch_id)
print("Batch status:", batch_info.status)

if batch_info.status != "completed":
    print("Batch is not completed yet. Please wait.")
    exit()

# === Step 4: Download result file ===
output_file_id = batch_info.output_file_id
if not output_file_id:
    print("No output file ID found — batch may have failed or had no valid results.")
    if batch_info.error_file_id:
        print("See error file ID:", batch_info.error_file_id)
    exit()

content = openai.files.content(output_file_id).read().decode("utf-8")
responses = [json.loads(line) for line in content.strip().split("\n") if line.strip()]

# === Step 5: DEBUG - print sample structure ===
print("Sample response structure:")
print(json.dumps(responses[0], indent=2))

# === Step 6: Extract cleaned outputs from new structure ===
cleaned_outputs = []

for i, r in enumerate(responses):
    try:
        content = r["response"]["body"]["choices"][0]["message"]["content"]
        cleaned_outputs.append(content)
    except (KeyError, IndexError, TypeError) as e:
        print(f"[Warning] Missing content at index {i}: {e}")
        print(json.dumps(r, indent=2))
        cleaned_outputs.append("")

# === Step 7: Load original dataset ===
try:
    df = pd.read_csv("data/sports_hobbies_records_to_clean.txt", sep="\t", engine="python", on_bad_lines="skip")
except Exception as e:
    print(f"Failed to read input file: {e}")
    exit()

# === Step 8: Truncate original to match results ===
if len(df) > len(cleaned_outputs):
    print(f"Warning: Truncating original file from {len(df)} to {len(cleaned_outputs)} rows.")
    df = df.iloc[:len(cleaned_outputs)]
elif len(df) < len(cleaned_outputs):
    print(f"Warning: Fewer input rows than cleaned outputs. Truncating results to {len(df)}.")
    cleaned_outputs = cleaned_outputs[:len(df)]

# === Step 9: Add cleaned data to DataFrame ===
df["clean_data"] = cleaned_outputs

# === Step 10: Save to output file ===
output_filename = "results/sports_hobbies_cleaned_with_predictions.csv"
df.to_csv(output_filename, index=False, encoding="utf-8-sig")
print(f"[Success] Saved: {output_filename}")

# === Step 11: Optional - Show error file if exists ===
if batch_info.error_file_id:
    print("\n[Info] There were errors in the batch. Downloading error file...")
    error_content = openai.files.content(batch_info.error_file_id).read().decode("utf-8")
    print("Error file contents:\n", error_content)