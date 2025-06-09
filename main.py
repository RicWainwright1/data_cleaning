import openai
import json
import os
import time
import os
from tqdm import tqdm
from datetime import datetime


openai.api_key = os.getenv("OPENAI_API_KEY")

def use_fine_tuned_model(model_name, user_prompt):
    response = OpenAI.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ]
    )
    print("🤖", response.choices[0].message.content.strip())

# ------------ CONFIGURATION ------------
BASE_MODEL = "gpt-3.5-turbo"
TRAIN_FILE = "train.jsonl"
TEST_FILE = "test.jsonl"
MODEL_SUFFIX = "favourite-sports-cleaners"
# ---------------------------------------

def upload_training_file(file_path):
    with open(file_path, "rb") as f:
        upload = openai.files.create(file=f, purpose="fine-tune")
    print(f"📤 Uploaded training file: {upload.id}")
    return upload.id

def create_fine_tune_job(training_file_id, base_model=BASE_MODEL, suffix=MODEL_SUFFIX):
    job = openai.fine_tuning.jobs.create(
        training_file=training_file_id,
        model=base_model,
        suffix=suffix
    )
    print(f"🧠 Fine-tuning job created: {job.id}")
    return job.id

def monitor_fine_tune(job_id):
    print(f"⏳ Monitoring fine-tune job {job_id}...")
    while True:
        job = openai.fine_tuning.jobs.retrieve(job_id)
        print(f"Status: {job.status}")
        if job.status in ["succeeded", "failed"]:
            break
        time.sleep(15)
    print(f"✅ Job completed with status: {job.status}")
    return job

def infer_with_model(model_name, question, raw_answer):
    response = openai.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": """You are a data cleaning assistant. Your job is to clean and standardize open-ended survey responses to ensure they are valid, verified, and formatted consistently.
            \n\nFollow these cleaning rules strictly:\n\n1. Blank or Ambiguous Responses\n
            - If the response is blank, null, or ambiguous (e.g., \"none\", \"n/a\", \"don't know\", \"idk\", \"I don\u2019t have one\"), return None.
            \n\n2. Keyboard Smashing, Gibberish, or Nonsense\n- If the response contains unrecognizable, random text (e.g., \"asdfgh\", \"qwerty\", \"jnrbcfbcj\", \"@#$$%\") with no valid words or known entities, return None.
            \n- Use heuristics such as: non-dictionary words, lack of vowels, too many repeated letters/symbols, or absence of contextually valid content.
            \n- If the response consists of numbers only, or sequences of characters that do not resemble known words or a valid answer (e.g., \"123456\", \"00000\", \"987654321\"), return [REVIEW].
            \n\n3. Context Validation\n- Ensure the response refers to a real, recognized entity or concept in context (e.g., a valid team, brand, location, etc.).\n- If it does not, return [REVIEW].
            \n\n4. Normalization and Standardization\n- Correct misspellings, abbreviations, or informal names.
            \n- Expand shorthand or nicknames (e.g., \"Barca\" \u2192 \"FC Barcelona\", \"Man U\" \u2192 \"Manchester United\").
            \n- Expand known acronyms or initials into full official names (e.g., \"MUFC\" \u2192 \"Manchester United\", \"CFC\" \u2192 \"Chelsea\", \"PSG\" \u2192 \"Paris Saint-Germain\").
            \n- Use Title Case formatting consistently (e.g., \"fc barcelona\" \u2192 \"FC Barcelona\").\n\n5. 
            Remove Qualifiers\n- Eliminate introductory phrases like \"I like\", \"My favorite is\", \"The best one is\".\n- Return only the cleaned core entity (e.g., \"I like the Lakers\" \u2192 \"Los Angeles Lakers\").
            \n\n6. Multiple Answers\n- If multiple valid items are listed and one is clearly more prominent, select that.\n- If the list is subjective, vague, or evenly weighted, return [REVIEW].\n"""},
            {"role": "user", "content": f"Question: {question}\nAnswer: {raw_answer}"}
        ],
        temperature=0
    )
    result = response.choices[0].message.content.strip()

    return result


def evaluate_on_test_set(model_name):
    print("\n📊 Evaluating on test set...\n")
    with open(TEST_FILE, "r") as f:
        test_data = [json.loads(line) for line in f]

    for i, item in enumerate(test_data):
        question = item["messages"][1]["content"].split("\n")[0].replace("Question: ", "")
        raw_answer = item["messages"][1]["content"].split("\n")[1].replace("Answer: ", "")
        expected_output = item["messages"][2]["content"]

        prediction = infer_with_model(model_name, question, raw_answer)

        print(f"{i+1}. Raw: {raw_answer}")
        print(f"   Cleaned: {prediction}")
        print(f"   Expected: {expected_output}")
        print("---")

import pandas as pd

def evaluate_cleaned_answers_to_dataframe(model):
    rows = []  
    # Load dataset
    with open(TEST_FILE, "r") as f:
        test_data = [json.loads(line) for line in f]

    for i, item in enumerate(test_data):
        question = item["messages"][1]["content"].split("\n")[0].replace("Question: ", "")
        raw_answer = item["messages"][1]["content"].split("\n")[1].replace("Answer: ", "")
        expected_output = item["messages"][2]["content"]

        prediction = infer_with_model(model_name, question, raw_answer)

        # Append to list
        rows.append({
            "index": i + 1,
            "raw": raw_answer,
            "expected": expected_output,
            "predicted": prediction,
            "correct": int(prediction.lower() == expected_output.lower())
        })

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Calculate accuracy
    accuracy = df["correct"].mean()
    print(f"\n✅ Accuracy: {accuracy:.2%} ({df['correct'].sum()}/{len(df)})")

    return df


# -------- MAIN FLOW --------
if __name__ == "__main__":
    # training_file_id = upload_training_file(TRAIN_FILE)
    # job_id = create_fine_tune_job(training_file_id)

    job_id = 'ftjob-oeZZXSvMmddi6UskSV1qjPIJ'

    job = monitor_fine_tune(job_id)

    if job.status == "succeeded":
        model_name = job.fine_tuned_model
        # evaluate_on_test_set(model_name)
        df_results = evaluate_cleaned_answers_to_dataframe(model_name)
        df_results.to_csv("evaluation_results_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv", index=False)
