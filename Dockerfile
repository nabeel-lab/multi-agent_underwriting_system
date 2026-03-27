# Multi-stage build: Frontend + Backend in one container

# Stage 1: Build Next.js frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/front
COPY front/package*.json ./
RUN npm ci
COPY front/ ./
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Stage 2: Python backend with frontend
FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY underwriting/ ./underwriting/
COPY serve_frontend.py .

# Copy built frontend
COPY --from=frontend-builder /app/front/.next/standalone ./front/.next/standalone
COPY --from=frontend-builder /app/front/.next/static ./front/.next/static
COPY --from=frontend-builder /app/front/public ./front/public
COPY static/ ./static/

# Copy .env file
COPY underwriting/.env ./underwriting/.env

# Expose port
EXPOSE 8080

# Run the combined server
CMD ["python", "serve_frontend.py"]
