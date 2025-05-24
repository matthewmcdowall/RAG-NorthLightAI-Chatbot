# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port used by uvicorn
EXPOSE 10000

# Run FastAPI app
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "10000"]
