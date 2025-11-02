# make_data.py
import json

data = {
    "labels": ["Jan","Fév","Mar","Avr","Mai","Juin"],
    "revenu": [1200, 1350, 1420, 1600, 1550, 1700],
    "users": [220, 245, 260, 280, 300, 315]
}

with open("data/series.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("✅ Données écrites dans data/series.json")
