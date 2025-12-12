# Multi-stage build for frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Python backend stage
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY env.example .env

# Copy built frontend into backend static folder
COPY --from=frontend-build /app/frontend/dist ./static

# Expose ports
EXPOSE 8000
EXPOSE 80

# Start backend API server
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
