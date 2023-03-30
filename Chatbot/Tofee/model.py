from transformers import pipeline

classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
labels = ["entertainment", "food and drink", "home", "lifestyle", "transportation", "utilities"] 
hypothesis_template = 'This text is about {}.'