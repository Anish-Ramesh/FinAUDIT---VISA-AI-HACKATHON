#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node dependencies and build frontend
cd frontend
npm install
npm run build
cd ..

# Copy frontend build to backend static folder for self-contained serving
mkdir -p backend/static
cp -r frontend/dist/* backend/static/
