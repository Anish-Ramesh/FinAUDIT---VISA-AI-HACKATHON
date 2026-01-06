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

# Serve React static files (Production Config - Robust)
# This handles the difference between local (backend/ as cwd) and Render (root as cwd)
BASE_DIR = Path(__file__).resolve().parent
# Navigate up to root, then into frontend/dist
# Structure:
# /root
#   /backend/main.py (Base Dir)
#   /frontend/dist/
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"
ASSETS_DIR = FRONTEND_DIST / "assets"

print(f"🔹 [Static Config] Serving frontend from: {FRONTEND_DIST}")

if FRONTEND_DIST.exists():
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
        target_file = FRONTEND_DIST / full_path
        if target_file.is_file():
            return FileResponse(target_file)
            
        # 3. Fallback to index.html for all other routes (SPA handling)
        return FileResponse(FRONTEND_DIST / "index.html")
else:
    print(f"❌ [Static Config] Frontend dist not found at {FRONTEND_DIST}")
    @app.get("/")
    def read_root():
        return {"status": "backend-running", "message": "Frontend build not found. Run 'npm run build' in frontend/"}
