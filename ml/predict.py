import joblib

# Eğitilmiş modeli yükle
model = joblib.load("model/model.joblib")

def predict_intent(text: str) -> str:
    """Verilen metinden intent (eylem) tahmini yapar."""
    prediction = model.predict([text])[0]
    return prediction

if __name__ == "__main__":
    while True:
        user_input = input("Sen: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        action = predict_intent(user_input)
        print(f"→ Tahmin edilen eylem: {action}")
