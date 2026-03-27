# Use Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install flask flask-cors requests

# Expose port
EXPOSE 5000

# Run backend
CMD ["python", "backend/app.py"]