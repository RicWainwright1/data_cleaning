
import pandas as pd
import json
import uuid

# Load the input TSV file
input_file = "sports_hobbies_records_to_clean.txt"
df = pd.read_csv(input_file, sep="\t", on_bad_lines='skip', engine="python")

{
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "ft:gpt-3.5-turbo-0125:your-org:sports-cleaning-v1:abc123xyz",
    "messages": [
      {"role": "system", "content": "You are a data cleaning assistant..."},
      {"role": "user", "content": "Question: What is your favourite sports team?\nAnswer: $$$raw_input$$$"}
    ]
  }
}


