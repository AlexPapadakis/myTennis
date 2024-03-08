from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
print("Engine created")


def get_db():
    print("Getting db...")
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("Session local created")

        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"Error occurred while connecting to database: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        db.close()
