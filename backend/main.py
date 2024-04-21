from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
import app.schemas as schemas
from app.routes.user import router as user_router
from app.routes.venue import router as venue_router
from app.routes.athlete import router as athlete_router
from app.routes.match import router as match_router
from app.routes.match_invitation import router as match_invitation_router
from app.routes.match_score import router as match_score_router
from app.routes.auth import router as auth_router
from app.routes.tournament import router as tournament_router

def initialize_app():
    schemas.Base.metadata.create_all(bind=engine)
    print("Tables defined by schemas created")

    app = FastAPI()
    origins = [
    "http://localhost:5173",  # React's port
    # add more origins if needed
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("App created")
        
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(venue_router)
    app.include_router(athlete_router)
    app.include_router(match_router)
    app.include_router(match_invitation_router)
    app.include_router(match_score_router)
    app.include_router(tournament_router)
    
    print("Routers included")


    return app

app = initialize_app()