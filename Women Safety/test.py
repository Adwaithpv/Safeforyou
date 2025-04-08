# Import the text classification pipeline from the Hugging Face transformers library
from transformers import pipeline

# Initialize the text classification pipeline using a multilingual DistilBERT model
# This model supports multiple languages including Hindi, English, etc.
classifier = pipeline(
    "text-classification",  # Task: text classification
    model="distilbert-base-multilingual-cased"  # Pretrained multilingual DistilBERT model
)

# Hindi input text for sentiment classification
input_text = "यह एक शानदार अनुभव था।"  # Translation: "This was a wonderful experience."

# Perform classification using the pipeline
result = classifier(input_text)

# Print the classification result
print(result)
