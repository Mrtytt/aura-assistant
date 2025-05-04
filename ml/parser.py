import os
import re
import json

# JSON dosyasından dataset'i yükle
with open('data/dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Önişlem: tüm input'ları lowercase'e çevir ve regex-safe yap
# dataset: [{"input": ..., "action": ...}, ...]
dataset_prepared = [
    {"pattern": re.escape(item["input"].lower()), "action": item["action"]}
    for item in dataset
]

# NLP ayrıştırıcı
def parse_nl_command(raw: str):
    """
    Gelen doğal dil komutunu dataset'teki kalıplarla eşleştirir.
    Eşleşen pattern temelinde action ve parametre sözlüğü döner.
    """
    text = raw.strip().lower()

    # Özel create_file kalıbı: <yer> klasörüne <dosya_adi> adlı bir <tur> dosyası oluştur
    m = re.match(
        r"^(.+?klasör(?:üne|e)?)[ \t]+(.+?)\s+adlı\s+(?:bir\s+)?(\w+)\s+dosyası oluştur",
        text
    )
    if m:
        loc = m.group(1).strip()
        name = m.group(2).strip()
        ftype = m.group(3).strip()
        return "create_file", {"yer": loc, "dosya_adi": name, "tur": ftype}

    # Diğer kalıplar
    for entry in dataset_prepared:
        pat = r'^' + entry["pattern"]
        m2 = re.match(pat, text)
        if m2:
            action = entry["action"]
            param_str = text[m2.end():].strip()
            params = param_str.split() if param_str else []
            return action, {"params": params}

    # Eşleşme yoksa fallback
    parts = text.split()
    return parts[0], {"params": parts[1:]}

# Örnek kullanım
if __name__ == "__main__":
    print("NLP parser hazır. dataset.json'a göre çalışıyor.")
    while True:
        raw = input("Komut> ")
        if raw.lower() in ['exit', 'çıkış']:
            break
        action, params = parse_nl_command(raw)
        print(f"action: {action}")
        for k, v in params.items():
            print(f"  {k}: {v}")
        print()
