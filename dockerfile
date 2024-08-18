# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make sure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script as the entrypoint for the container
ENTRYPOINT ["/app/entrypoint.sh"]

# Run main.py when the container launches
CMD ["python", "main.py"]