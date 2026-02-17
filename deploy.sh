#!/bin/bash

# FIX WINDOWS LINE ENDINGS (JUST IN CASE)
# This removes carriage returns if the file was uploaded from Windows
sed -i 's/\r$//' "$0"

echo "🚀 STARTING DEPLOYMENT..."

# 1. CREATE WEIGHTS DIRECTORY IF NOT EXISTS
if [ ! -d "weights" ]; then
    echo "📂 CREATING WEIGHTS DIRECTORY..."
    mkdir -p weights
fi

# 2. CHECK FOR MODEL WEIGHTS (DOWNLOAD IF MISSING)
echo "🔍 CHECKING MODEL WEIGHTS..."

if [ ! -f "weights/GFPGANv1.3.pth" ]; then
    echo "⬇️ DOWNLOADING GFPGAN WEIGHTS..."
    wget -q --show-progress https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth -P weights/
else
    echo "✅ GFPGAN WEIGHTS FOUND."
fi

if [ ! -f "weights/RealESRGAN_x4plus.pth" ]; then
    echo "⬇️ DOWNLOADING REAL-ESRGAN WEIGHTS..."
    wget -q --show-progress https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P weights/
else
    echo "✅ REAL-ESRGAN WEIGHTS FOUND."
fi

# 3. BUILD AND RUN CONTAINERS
echo "🐳 BUILDING CONTAINERS..."

# CHECK IF docker compose OR docker compose IS AVAILABLE
if command -v docker compose &> /dev/null; then
    docker compose down
    docker compose up --build -d
else
    # NEWER DOCKER VERSIONS USE 'docker compose' (NO HYPHEN)
    docker compose down
    docker compose up --build -d
fi

echo "✅ DEPLOYMENT COMPLETE! SYSTEM RUNNING ON PORT 3000."