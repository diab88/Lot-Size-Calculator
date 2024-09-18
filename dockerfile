# Step 1: Use an official Python runtime as a base image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose port 5000 to the outside world (Flask default port)
EXPOSE 5000

# Step 6: Define environment variable to allow Flask to run
ENV FLASK_APP=app.py

# Step 7: Run Flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
