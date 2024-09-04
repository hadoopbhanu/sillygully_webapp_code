# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and PyMySQL
RUN pip install flask pymysql

# Expose the port that the Flask app runs on
EXPOSE 8080

# Define environment variables
ENV DB_USER=sqladmin
ENV DB_PASSWORD=admin
ENV DB_NAME=world_metrics
ENV DB_HOST=192.168.0.21 

# Run the application
CMD ["python", "app.py"]
