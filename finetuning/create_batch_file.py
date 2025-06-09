import pandas as pd
import json
import uuid
# Load the input TSV file
input_file = "sports_hobbies_records_to_clean.txt"
df = pd.read_csv(input_file, sep="\t", on_bad_lines='skip', engine="python")

# Define the master prompt
system_prompt = """You are a data cleaning assistant. Your job is to clean and standardize open-ended survey responses to ensure they are valid, verified, and formatted consistently.

Follow these cleaning rules strictly:

1. Blank or Ambiguous Responses
- If the response is blank, null, or ambiguous (e.g., "none", "n/a", "don't know", "idk", "I don’t have one"), return None.

2. Keyboard Smashing, Gibberish, or Nonsense
- If the response contains unrecognizable, random text (e.g., "asdfgh", "qwerty", "jnrbcfbcj", "@#$$%") with no valid words or known entities, return None.
- Use heuristics such as: non-dictionary words, lack of vowels, too many repeated letters/symbols, or absence of contextually valid content.
- If the response consists of numbers only, or sequences of characters that do not resemble known words or a valid answer (e.g., "123456", "00000", "987654321"), return [REVIEW].

3. Context Validation
- Ensure the response refers to a real, recognized entity or concept in context (e.g., a valid team, brand, location, etc.).
- If it does not, return [REVIEW].

4. Normalization and Standardization
- Correct misspellings, abbreviations, or informal names.
- Expand shorthand or nicknames (e.g., "Barca" → "FC Barcelona", "Man U" → "Manchester United").
- Expand known acronyms or initials into full official names (e.g., "MUFC" → "Manchester United", "CFC" → "Chelsea", "PSG" → "Paris Saint-Germain").
- Use Title Case formatting consistently (e.g., "fc barcelona" → "FC Barcelona").

5. Remove Qualifiers
- Eliminate introductory phrases like "I like", "My favorite is", "The best one is".
- Return only the cleaned core entity (e.g., "I like the Lakers" → "Los Angeles Lakers").

6. Multiple Answers
- If multiple valid items are listed and one is clearly more prominent, select that.
- If the list is subjective, vague, or evenly weighted, return [REVIEW].
"""

model_id = "ft:gpt-3.5-turbo-0125:the-insights-family:favourite-sports-cleaners:BYwH5kjs"

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
                {"role": "system", "content": system_prompt},
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
