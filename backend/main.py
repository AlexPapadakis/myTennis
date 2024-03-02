from fastapi import FastAPI
from app.database import engine
import app.models as models
from app.routes.user import router as user_router
from app.routes.venue import router as venue_router

def initialize_app():
    models.Base.metadata.create_all(bind=engine)
    print("Tables defined by models created")

    app = FastAPI()
    print("App created")
    
    app.include_router(user_router)
    app.include_router(venue_router)
    print("Router included")


    return app

app = initialize_app()