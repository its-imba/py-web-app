# Using latest python version with slim variant (reduction of 900mb -> 170mb container size)
FROM python:3.11-slim-bullseye
WORKDIR /app

# Copy only the requirements.txt file first
COPY requirements.txt .

# Install Python dependencies only if requirements.txt has changed to speed up image creation by using a cache mount
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 5000 to access container
EXPOSE 5000

# Set the entrypoint command to execute the main.py file
ENTRYPOINT ["python", "main.py"]
