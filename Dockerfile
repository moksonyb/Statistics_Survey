# Use an official Python image as the base
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy your application code into the container
COPY app.py .

# Install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app listens on (if needed)
EXPOSE 5000

# Specify the command to run your app
CMD ["python", "app.py"]
