from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import requests
from datetime import datetime

# FastAPI instance
app = FastAPI(docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database URL
DATABASE_URL = "postgresql://postgres:aezakmi%401@143.244.128.109/weather"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define your table schema
class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create the table if not exists
Base.metadata.create_all(bind=engine)

# Pydantic model for request body
class WeatherDataIn(BaseModel):
    city: str

# Pydantic model for response body
class WeatherDataOut(BaseModel):
    city: str
    temperature: float
    humidity: float
    wind_speed: float
    timestamp: datetime

    class Config:
        orm_mode = True

# OpenWeatherMap API key
API_KEY = "ac5559a726f0d448e4c774c8fa2c6655"

# Function to fetch weather data from OpenWeatherMap
def fetch_weather_data(city: str):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": datetime.utcnow()
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching weather data: {str(e)}")

# Routes
@app.post("/weather/", response_model=WeatherDataOut)
async def create_weather_data(weather_data_in: WeatherDataIn):
    session = SessionLocal()
    try:
        db_weather_data = session.query(WeatherData).filter(WeatherData.city == weather_data_in.city).first()
        if db_weather_data:
            return db_weather_data

        weather_data = fetch_weather_data(weather_data_in.city)
        db_weather_data = WeatherData(**weather_data)
        session.add(db_weather_data)
        session.commit()
        session.refresh(db_weather_data)
        return db_weather_data
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@app.get("/weather/{city}/", response_model=WeatherDataOut)
async def read_weather_data(city: str):
    session = SessionLocal()
    try:
        weather_data = fetch_weather_data(city)
        db_weather_data = WeatherData(**weather_data)
        session.add(db_weather_data)
        session.commit()
        session.refresh(db_weather_data)
        return db_weather_data
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@app.get("/weather/{city}/all", response_model=List[WeatherDataOut])
async def read_all_weather_data(city: str):
    session = SessionLocal()
    try:
        weather_data_list = session.query(WeatherData).filter(WeatherData.city == city).all()
        return weather_data_list
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
