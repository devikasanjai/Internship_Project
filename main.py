from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Float # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

app = FastAPI()

# Database URL
DATABASE_URL = "postgresql://devikasanjai:devxkaa03@localhost/postgres"
# Update with your actual password if set

# SQLAlchemy
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

# Create the table if not exists
Base.metadata.create_all(bind=engine)

# Pydantic model for request body
class WeatherDataIn(BaseModel):
    city: str
    temperature: float
    humidity: float
    wind_speed: float

# Pydantic model for response body
class WeatherDataOut(BaseModel):
    id: int
    city: str
    temperature: float
    humidity: float
    wind_speed: float

    class Config:
        from_attributes = True

# Routes
@app.post("/weather/", response_model=WeatherDataOut)
async def create_weather_data(weather_data: WeatherDataIn):
    session = SessionLocal()
    try:
        db_weather_data = WeatherData(**weather_data.dict())
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
async def read_weather_data(request: Request, city: str):
    session = SessionLocal()
    try:
        weather_data = session.query(WeatherData).filter(WeatherData.city == city).first()
        if weather_data is None:
            raise HTTPException(status_code=404, detail="Weather data not found")
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
