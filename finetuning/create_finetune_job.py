import openai
import os

# Authenticate
openai.api_key = os.getenv("OPENAI_API_KEY") # Replace with your real key

file_id = "file-Pex2PRYKucxEV38M8YWjk9"


# Replace with a fine-tuneable model like gpt-3.5-turbo
fine_tune_job = openai.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-4.1-nano-2025-04-14",
    suffix="sports-cleaning-v1",
    metadata={"job_name": "Sports Data Cleaning Job v1"}
)

print("Fine-tune Job ID:", fine_tune_job.id)