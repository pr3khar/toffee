from transformers import pipeline

# Classify text using the zero-shot-classification pipeline
def classify_text(text):
    classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    labels = ["entertainment", "food and drink", "home", "lifestyle", "transportation", "utilities"] 
    hypothesis_template = 'This text is about {}.'

    results = classifier(text, labels, hypothesis_template=hypothesis_template)
    if results['scores'][0] >= 0.85:
        category = results['labels'][0]

    elif results['scores'][0] >= 0.65 and results['scores'][1] >= 0.65 and results['scores'][2] >= 0.65:
        category = "Miscellaneous"
    elif all(x <= 0.2 for x in results['scores']):
        category = "Miscellaneous"
    
    return category

