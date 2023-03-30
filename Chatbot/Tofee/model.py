from transformers import pipeline

# Classify text using the zero-shot-classification pipeline
def classify_text(text):
    classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    labels = ["entertainment", "food and drink", "home", "lifestyle", "transportation", "utilities"] 
    hypothesis_template = 'This text is about {}.'

    results = classifier(text, labels, hypothesis_template=hypothesis_template)
    category = results['labels'][0]

    return category

