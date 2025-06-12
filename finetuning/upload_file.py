import openai
import os


# Authenticate
openai.api_key = os.getenv("OPENAI_API_KEY") # Replace with your real key

# Upload the file to OpenAI's servers
file = openai.files.create(
    file=open("finetuned_sports_hobbies_cleaning_batch.jsonl", "rb"),
    purpose="fine-tune"
)

print("File ID:", file.id)

