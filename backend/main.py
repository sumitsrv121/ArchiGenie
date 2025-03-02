from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
import os
import logging
from backend.api import router
from backend.limiter import limiter  # Import shared limiter

logging.basicConfig(level=logging.DEBUG)

# Initialize the limiter first and attach to app state.
app = FastAPI(title="ArchiGenie API")
app.state.limiter = limiter

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000)
