from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import users_router, fundraiser_router, donation_router, stats_router, platform_stats_router, success_story_router
import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Crowd funding website running",
    redirect_slashes=True
)

#  Broad but specific CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB tables
Base.metadata.create_all(bind=engine)

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

# Routers
app.include_router(users_router.router)
app.include_router(fundraiser_router.router)
app.include_router(donation_router.router)
app.include_router(stats_router.router)
app.include_router(platform_stats_router.router)
app.include_router(success_story_router.router)

@app.get("/")
def greet():
    return {
        "status": "online",
        "message": "LifeGivers API is running - Dual Origin CORS Fix",
        "version": "1.0.3"
    }
