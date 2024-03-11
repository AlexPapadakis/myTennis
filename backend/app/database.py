from sqlalchemy import create_engine,exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
print("Engine created")


def create_session_local():
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("Session local created")
        return SessionLocal
    except Exception as e:
        print(f"Error occurred while creating SessionLocal: {e}")
        raise HTTPException(status_code=500, detail="SessionLocal creation error")

def create_db_session(SessionLocal):
    try:
        db = SessionLocal()
        print("DB session created")
        return db
    except Exception as e:
        print(f"Error occurred while creating DB session: {e}")
        raise HTTPException(status_code=500, detail="DB session creation error")

def get_db():
    SessionLocal = create_session_local()
    db = create_db_session(SessionLocal)
    try:
        yield db
    except exc.SQLAlchemyError as e:
        print(f"Error occurred while connecting to database: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        if db is not None:
            db.close()