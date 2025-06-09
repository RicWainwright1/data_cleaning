import random
import json

# Load full dataset
with open("sports_team_cleaning_dataset_part5.jsonl", "r") as f:
    data = [json.loads(line) for line in f]

# Shuffle for randomness
random.seed(42)
random.shuffle(data)

# Split
train_data = data[:700]
test_data = data[700:900]
val_data = data[900:]

# Save splits
def save_jsonl(filename, dataset):
    with open(filename, "w") as f:
        for item in dataset:
            f.write(json.dumps(item) + "\n")

save_jsonl("train.jsonl", train_data)
save_jsonl("test.jsonl", test_data)
save_jsonl("validation.jsonl", val_data)

print("✅ Split complete: train (700), test (200), validation (100)")
