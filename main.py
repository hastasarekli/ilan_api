from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS izinleri (Android’den veri çekmek için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Örnek veriler (500.000–700.000 TL arası)
with open("sample_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

@app.get("/search")
def search(
    marka: str = Query(...),
    model: str = Query(...),
    yil_min: int = Query(2000),
    yil_max: int = Query(2025),
    km_max: int = Query(200000),
    fiyat_min: int = Query(0),
    fiyat_max: int = Query(1000000)
):
    results = []
    for ilan in data:
        if (marka.lower() in ilan["arac"].lower() and
            model.lower() in ilan["arac"].lower() and
            yil_min <= ilan["yil"] <= yil_max and
            ilan["km"] <= km_max and
            fiyat_min <= ilan["fiyat"] <= fiyat_max):
            results.append(ilan)
    return {"results": results}

@app.get("/detail")
def detail(url: str):
    for ilan in data:
        if ilan["url"] == url:
            return ilan
    return {"error": "İlan bulunamadı"}
