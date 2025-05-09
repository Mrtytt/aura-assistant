from transformers import pipeline

classifier = pipeline("text-classification", model="my-intent-classifier")

while True:
    text = input(">> ")
    result = classifier(text)[0]
    print(f"Intent: {result['label']} (confidence: {result['score']:.2f})")
