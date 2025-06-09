import openai
import os

# Authenticate
openai.api_key = os.getenv("OPENAI_API_KEY") # Replace with your real key

# Upload the JSONL file
upload_response = openai.files.create(
    file=open("sports_hobbies_cleaning_batch.jsonl", "rb"),
    purpose="batch"
)

# Create the batch job
batch_job = openai.batches.create(
    input_file_id=upload_response.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",  # use '24h' or '1h' if supported
    metadata={
        "job_type": "Sports & Hobbies Cleaning"
    }
)

print("Batch Job ID:", batch_job.id)


