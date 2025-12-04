
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


	# Install system dependencies + SSL certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential gcc ca-certificates postgresql-client \
	&& rm -rf /var/lib/apt/lists/*


# Copy requirements first to leverage Docker layer caching
COPY requirements.txt /app/

RUN python -m pip install --upgrade pip \
	&& pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code (do NOT copy secrets or .env into the image)
COPY . /app

# Copy wait-for-db script and make it executable
COPY wait-for-db.sh /app/wait-for-db.sh
RUN chmod +x /app/wait-for-db.sh

# Expose the port used by the app
EXPOSE 8000

# Use a tiny entrypoint that waits for the DB to be ready, then start uvicorn.
ENTRYPOINT ["/app/wait-for-db.sh", "db"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]