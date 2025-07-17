from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routes.player_routes import router as player_router
from .db.database import engine
from sqlmodel import SQLModel

# Lifespan event for database initialization
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# Create FastAPI app instance with lifespan event
app = FastAPI(lifespan=lifespan)

# Set up CORS middleware for cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (e.g., player routes)
app.include_router(player_router)

# Mount static files directory (for serving images, if needed)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Add any other middleware or configuration (logging, error handling, etc.) as needed.