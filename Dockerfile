# Start from an official Python base image. "slim" is a smaller,
# stripped-down version — fewer extras means a lighter, faster image.
FROM python:3.12-slim

# Set the working directory inside the image. Everything after this
# happens in /app, and it's created if it doesn't exist.
WORKDIR /app

# Copy ONLY requirements first, then install. This ordering is deliberate
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your application code into the image.
COPY . .

# Document that the app listens on port 8000.
EXPOSE 8000

# The command that runs when a container starts from this image.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
