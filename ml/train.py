
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib

# Veri dosyasını oku
with open("data/dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["input"] for item in data]
labels = [item["action"] for item in data]

# Model pipeline: TF-IDF + Lojistik Regresyon
model = make_pipeline(
    TfidfVectorizer(),
    LogisticRegression(max_iter=1000)
)

# Modeli eğit
model.fit(texts, labels)

# Modeli kaydet
joblib.dump(model, "model/model.joblib")

print("Model başarıyla eğitildi ve kaydedildi.")
