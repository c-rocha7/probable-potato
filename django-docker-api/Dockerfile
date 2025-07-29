# Use Python 3.13 slim image
FROM python:3.13.4-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apk update \
    && apk add --no-cache \
        postgresql-client \
        build-base \
        postgresql-dev \
        linux-headers \
    && rm -rf /var/cache/apk/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Make wait-for-db.sh executable
RUN chmod +x /app/wait-for-db.sh

# Expose port
EXPOSE 8000

# Run the application using our wait script
CMD ["./wait-for-db.sh"]
