from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Financial Data Health & Compliance System",
    description="Metadata-only regulatory compliance checking system.",
    version="0.1.0"
)

# CORS Setup - Allow All for Render/Demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for Render deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

# ... (existing code)

from api.endpoints import router as api_router
app.include_router(api_router, prefix="/api")

# Serve React static files (Production Config - Self-Contained)
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
ASSETS_DIR = STATIC_DIR / "assets"

print(f"🔹 [Static Config] Serving frontend from: {STATIC_DIR}")

if STATIC_DIR.exists():
    # Mount assets folder (JS/CSS)
    if ASSETS_DIR.exists():
        app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
    
    # Catch-all for React Router (Single Page App)
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # 1. API requests are handled by the router strictly
        if full_path.startswith("api"):
            return {"error": "API Endpoint Not Found"}
            
        # 2. Serve specific file if it exists (e.g., favicon.ico, logo.png)
        target_file = STATIC_DIR / full_path
        if target_file.is_file():
            return FileResponse(target_file)
            
        # 3. Fallback to index.html for all other routes (SPA handling)
        return FileResponse(STATIC_DIR / "index.html")
else:
    print(f"❌ [Static Config] Static folder not found at {STATIC_DIR}")
    @app.get("/")
    def read_root():
        return {"status": "backend-running", "message": "Frontend build not found in backend/static/"}
