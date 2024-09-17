# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app to be accessible
EXPOSE 5000

# Define environment variable to tell Flask to run in production
ENV FLASK_ENV=production

# Command to run the Flask app
CMD ["python", "app.py"]
