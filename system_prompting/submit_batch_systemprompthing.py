import openai
import os

# Authenticate
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this env var is set

# Upload the JSONL batch input file
batch_file_path = "sports_hobbies_cleaning_batch_systemprompt.jsonl"
try:
    with open(batch_file_path, "rb") as file:
        upload_response = openai.files.create(
            file=file,
            purpose="batch"
        )
    print(f"✅ File uploaded. File ID: {upload_response.id}")
except Exception as e:
    print(f"❌ Failed to upload file: {e}")
    exit(1)

# Create the batch job using the uploaded file
try:
    batch_job = openai.batches.create(
        input_file_id=upload_response.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",  # Options: "1h", "24h"
        metadata={
            "job_type": "sports_hobbies_cleaning"
        }
    )
    print("✅ Batch job submitted.")
    print("Batch Job ID:", batch_job.id)
except Exception as e:
    print(f"❌ Failed to create batch job: {e}")
