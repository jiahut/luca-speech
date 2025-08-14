# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN uv pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Create and declare the output directory as a volume
RUN mkdir -p /app/output
VOLUME /app/output

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run server.py when the container launches
CMD ["python", "server.py"]
