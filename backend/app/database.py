from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException



encoded_password = "Kwdikos12!@".replace("@", "%40")
DATABASE_URL = f"postgresql://postgres:{encoded_password}@127.0.0.1:5432/myTennis"

engine = create_engine(DATABASE_URL)
print("Engine created")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("Session local created")


def get_db():
    print("Getting db...")
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"Error occurred while connecting to database: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        db.close()
