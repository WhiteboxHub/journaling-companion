# ---- Base image with Python and pip ----
FROM python:3.10-slim

# ---- Set work directory ----
WORKDIR /app

# ---- Install system-level dependencies ----
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy requirements and install ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy entire source code ----
COPY . .

# ---- Expose port ----
EXPOSE 8000

# ---- Run FastAPI app using uvicorn ----
CMD ["uvicorn", "src.api.emotion_api:app", "--host", "0.0.0.0", "--port", "8000"]
