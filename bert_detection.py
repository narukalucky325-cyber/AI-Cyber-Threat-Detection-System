
import pandas as pd

from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments
)

from datasets import Dataset
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv('datasets/ai_generated_emails.csv')

# Split data
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df['text'],
    df['ai_generated'],
    test_size=0.2,
    random_state=42
)

# Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenization
def tokenize(batch):
    return tokenizer(
        batch['text'],
        padding=True,
        truncation=True
    )

# Dataset conversion
train_dataset = Dataset.from_dict({
    'text': train_texts.tolist(),
    'label': train_labels.tolist()
})

train_dataset = train_dataset.map(tokenize, batched=True)

# Load BERT model
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2
)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-5,
    weight_decay=0.01
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

# Train model
trainer.train()

# Save model
model.save_pretrained('models/bert_model')
tokenizer.save_pretrained('models/bert_model')

print("BERT Model Saved")
