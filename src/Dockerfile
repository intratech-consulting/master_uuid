FROM python:3.9-slim

WORKDIR /app

# Install Flask and other dependencies directly
RUN pip install --no-cache-dir --force-reinstall Flask==3.0.3 mysql-connector-python==8.0.28

# Copy the application code into the container
COPY . .

# Set the command to run the Flask application
CMD ["python", "src/api.py"]