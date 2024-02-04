import torch
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
from datasets import load_dataset, DatasetDict
from sklearn.model_selection import train_test_split

# Load and prepare dataset
def load_and_prepare_data(file_path, test_size=0.2):
    raw_datasets = load_dataset('sentiment_analysis.csv', data_files=file_path)
    raw_train_dataset, raw_test_dataset = train_test_split(raw_datasets['train'], test_size=test_size)
    return DatasetDict({
        'train': raw_train_dataset,
        'test': raw_test_dataset
    })

# Tokenize the texts
def tokenize_function(examples, tokenizer):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

# Parameters
model_name = "bert-base-uncased"
batch_size = 4
file_path = "your_dataset.csv"  # Update this path to your dataset

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Load and preprocess the dataset
datasets = load_and_prepare_data(file_path)
tokenized_datasets = datasets.map(lambda examples: tokenize_function(examples, tokenizer), batched=True)

# Training and evaluation
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=3,
    weight_decay=0.01,
    evaluation_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

trainer.train()

# Save the fine-tuned model
model.save_pretrained("./fine_tuned_model")