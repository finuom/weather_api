from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests

app = FastAPI()

# Serve static files (like index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

API_KEY = "a745aed7df210118874cf537f43261fb"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/weather")
def get_weather(city: str = Query(...)):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=data.get("message", "City not found"))

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature_celsius": data["main"]["temp"],
        "weather": data["weather"][0]["description"],
        "humidity_percent": data["main"]["humidity"],
        "wind_speed_mps": data["wind"]["speed"]
    }