from transformers import pipeline

classifier = pipeline("text-classification", model="distilbert-base-multilingual-cased")
result = classifier("यह एक शानदार अनुभव था।")
print(result)