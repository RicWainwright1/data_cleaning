# Data Cleaning Project

A machine learning project for cleaning and standardizing open-ended survey responses related to sports teams and leagues using OpenAI's GPT models.

## Overview

This project provides two approaches for cleaning messy sports-related survey data:
1. **Fine-tuned Model Approach**: Train a custom GPT-3.5-turbo model on labeled examples
2. **System Prompting Approach**: Use detailed system prompts with GPT-4 for batch processing

## Project Structure

```
├── data/
│   ├── split_the_data.py              # Split dataset into train/test/validation
│   ├── train.jsonl                    # Training data (700 samples)
│   ├── test.jsonl                     # Test data (200 samples)
│   ├── golden_dataset   
│   └── validation.jsonl               # Validation data (100 samples)

├── system_prompting/
│   ├── create_batch_systemprompting.py    # Generate batch requests with system prompts
│   └── submit_batch_systemprompthing.py   # Submit batch job to OpenAI
├── finetuning/
│   ├── create_batch.py    # Generate batch requests with system prompts
│   ├── create_finetune_file.py
│   ├── create_finetune_job.py    # Generate batch requests with system prompts
├── main.py                            # Fine-tuning workflow and evaluation
├── submit_batch.py                    # Submit batch processing job
├── download_and_append_results.py     # Download and process batch results
└── requirements.txt                   # Python dependencies
```

## Features

### Data Cleaning Rules
The system applies comprehensive cleaning rules to handle:
- **Blank/Ambiguous Responses**: "none", "n/a", "idk" → `None`
- **Gibberish Detection**: "asdfgh", "qwerty" → `None`
- **Standardization**: "Barca" → "FC Barcelona", "Man U" → "Manchester United FC"
- **Format Normalization**: Remove qualifiers, fix encoding, handle special characters
- **Context Validation**: Ensure responses refer to real sports entities

### Supported Entities
- **Football/Soccer Teams**: Premier League, La Liga, Bundesliga, etc.
- **Basketball**: NBA teams
- **Formula 1**: Teams and championship
- **Tennis**: ATP/WTA tours
- **Various Leagues**: Worldwide football leagues, national competitions

## Setup

### Prerequisites
- Python 3.7+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sports-data-cleaning
```

These are all setup and handled by the environment variables
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Environment Variables (.env file)

To run this project securely, you'll need to provide environment-specific settings (such as API keys, database passwords, etc.) in a .env file located in the project root.

✅ Format of the .env file

The .env file should use simple KEY=VALUE pairs, one per line:

# Example .env file

```bash
DB_USER=your_username
DB_PASSWORD=your_password
API_KEY=your_api_key_here
ENV=development
```

⚠️ Important: Do not commit your .env file to version control. It's already excluded via .gitignore.
📋 To get started:

Copy the example file:
cp .env.example .env
Fill in your actual values in .env.

If using Python, install python-dotenv to load environment variables automatically:
```bash
pip install python-dotenv
```
In your Python scripts, load the variables like so:
```bash
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.getenv("DB_USER")
```


## How to create the conda environment

To create a Conda environment from an environment.yaml file, use the following command in your terminal after cd'ing in to the directory:
```bash
conda env create -f environment.yaml
```

You can then activate the environment using 
```bash
conda activate data_cleaning
```

To deactivate it you can use: 
```bash
conda deactivate
```

## Order to run the data cleaning in:

ALL OF THE FILES ARE IN THE DATA CLEANING REPO!

## Step 1 - create the finetuned file from the golden dataset
```bash
cd data_cleaning/finetuning
python create_finetune_file.py
```
this takes in the golden dataset (which is an excel file in the data folder) with questions, answers given, the prompt and the expected result. detailed prompt is called data_clean_prompt.py - this needs changing to a dynamic name so we can have multiple for different question types.

## Step 2 - Upload the file to openAI
```bash
python upload_file.py
```
this takes the file we generated earlier which is a jsonl file and uploads it to openAI - we then get a file ID.

## Step 3 - Create the finetune job
```bash
python create_finetune_job.py
```
create_finetune_job using the fileID we got earlier update line 7 with the ID from before - you can adjust the suffix and metadata to get better information. Logging in with the technology account you can see the following: https://platform.openai.com/finetune/ftjob-nFkJeGTgxhPiDNS6hCE3f6Np?filter=all - you will see the progress of the fine tuned model

Once the model has completed the tuning we can now run a batch of datacleaning. Firstly we need to create the batch...

## Step 4 - Create the batch datacleaning job
```bash
python create_batch_systemprompting.py
```
Similar to before this create the file format that OpenAI needs to run the file, you can adjust the model on row 114

## Step 5 - Submit the batch & kick off the batch job 
```bash
python submit_batch_systemprompting.py
```
submit_batch_systemprompting to see the progress go here: https://platform.openai.com/batches/batch_6847f4a15c1c8190bc7194339d14c088 this will give us an ID at the end.


Using the ID from the previous step update the batch_id on line 11 - the file sits in the root of the data_cleaning repo. 
## Step 5 - Submit the batch & kick off the batch job 
```bash
python download_and_append_results.py
```
The last step is to review the results and store them in the results folder for review.

## Monitoring and Evaluation

### Fine-tuning Monitoring
The fine-tuning process includes:
- Real-time job status monitoring
- Automatic completion detection
- Test set evaluation with accuracy metrics

### Batch Processing Monitoring
Check batch status using the OpenAI dashboard or API with your batch job ID.

## Error Handling

The project includes comprehensive error handling for:
- File upload failures
- Batch processing errors
- API rate limits
- Malformed data

## Best Practices

1. **Data Quality**: Ensure training data is well-labeled and diverse
2. **Model Selection**: Choose between fine-tuning (consistency) vs system prompting (flexibility)
3. **Batch Size**: For large datasets, use batch API for cost efficiency
4. **Validation**: Always review `[REVIEW]` flagged items manually

## Troubleshooting

### Common Issues
- **API Key**: Ensure `OPENAI_API_KEY` environment variable is set
- **File Paths**: Verify all input files exist in expected locations
- **Batch Status**: Allow sufficient time for batch job completion (up to 24h)

### Support
Check the OpenAI documentation for API-related issues:
- [Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Batch API Documentation](https://platform.openai.com/docs/guides/batch)
