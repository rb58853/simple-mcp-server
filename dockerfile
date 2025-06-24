FROM python:3.13-slim

# Set working directory
WORKDIR /

# Copy the rest of the application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "src.fast_api.api:app", "--host", "0.0.0.0", "--port", "8000"]