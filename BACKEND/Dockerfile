# USE STANDARD PYTHON IMAGE
FROM python:3.10-slim

WORKDIR /app

# INSTALL SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# INSTALL CPU VERSION OF PYTORCH
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# COPY REQUIREMENTS
COPY REQUIREMENTS.txt .

# INSTALL DEPENDENCIES
RUN pip install --no-cache-dir -r REQUIREMENTS.txt

# INSTALL GUNICORN (IMPORTANT)
RUN pip install gunicorn

# --- BASICSR FIX ---
RUN sed -i 's/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/' /usr/local/lib/python3.10/site-packages/basicsr/data/degradations.py || true

COPY . .

RUN mkdir -p /app/WEIGHTS

EXPOSE 8000

# RUN WITH LONG REQUEST TIMEOUT (10 MIN)
CMD ["gunicorn", "APP.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "600", "--workers", "1"]
