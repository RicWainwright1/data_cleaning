# Sports Data Cleaning Project

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
│   └── validation.jsonl               # Validation data (100 samples)
├── system_prompting/
│   ├── create_batch_systemprompting.py    # Generate batch requests with system prompts
│   └── submit_batch_systemprompthing.py   # Submit batch job to OpenAI
├── finetuning/
│   ├── create_batch.py    # Generate batch requests with system prompts
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

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Method 1: Fine-tuned Model Approach

#### 1. Prepare Training Data
```bash
python data/split_the_data.py
```
This creates train/test/validation splits from your dataset.

#### 2. Fine-tune the Model
```bash
python main.py
```
This script will:
- Upload training data to OpenAI
- Create a fine-tuning job
- Monitor training progress
- Evaluate the model on test data
- Generate evaluation results CSV

#### 3. Model Evaluation
The script automatically evaluates the fine-tuned model and saves results to:
- `evaluation_results_YYYY-MM-DD_HH-MM-SS.csv`

### Method 2: System Prompting with Batch API

#### 1. Prepare Batch Input
```bash
python system_prompting/create_batch_systemprompting.py
```
This generates `sports_hobbies_cleaning_batch_systemprompt.jsonl` for batch processing.

#### 2. Submit Batch Job
```bash
python system_prompting/submit_batch_systemprompthing.py
```
Returns a batch job ID for tracking.

#### 3. Download Results
```bash
python download_and_append_results.py
```
Downloads completed batch results and merges with original data.

## Configuration

### Fine-tuning Settings (main.py)
```python
BASE_MODEL = "gpt-3.5-turbo"
TRAIN_FILE = "train.jsonl"
TEST_FILE = "test.jsonl"
MODEL_SUFFIX = "favourite-sports-cleaners"
```

### Batch Processing Settings
- **Model**: GPT-4.1
- **Temperature**: 0 (deterministic output)
- **Completion Window**: 24 hours

## Output Formats

The system returns one of three possible outputs:
- **Cleaned Name**: Standardized entity name (e.g., "Chelsea FC")
- **None**: For invalid/ambiguous responses
- **[REVIEW]**: For questionable entries requiring human review

## Example Transformations

| Input | Output |
|-------|--------|
| "I like the Lakers" | "Los Angeles Lakers" |
| "Barca" | "FC Barcelona" |
| "Man U" | "Manchester United FC" |
| "asdfgh" | None |
| "idk" | None |
| "★Barcelona★" | "FC Barcelona" |

## File Descriptions

- **`main.py`**: Complete fine-tuning pipeline with evaluation
- **`split_the_data.py`**: Dataset splitting utility
- **`submit_batch.py`**: Basic batch job submission
- **`download_and_append_results.py`**: Batch results processing
- **`create_batch_systemprompting.py`**: Advanced batch input generation
- **`submit_batch_systemprompthing.py`**: Enhanced batch submission

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
