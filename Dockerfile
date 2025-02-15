FROM python:3.13-slim

# Prevents Python from writing .pyc files to disc and buffering stdout/stderr.
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the command to run the Flask app via Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
