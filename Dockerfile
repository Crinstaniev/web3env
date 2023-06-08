# Use the official Python base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

RUN apt-get update && apt-get install -y make

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the entire application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 8080

# Run the Flask application
CMD ["make", "flask"]
