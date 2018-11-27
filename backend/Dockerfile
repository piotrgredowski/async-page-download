FROM python:3.6-slim

WORKDIR /dependencies

# Install dependencies
COPY requirements.txt /dependencies
RUN pip3 install -r requirements.txt

# ONLY FOR DEVELOPMENT
COPY requirements-dev.txt /dependencies
RUN pip3 install -r requirements-dev.txt

# Copy whole current directory
WORKDIR /app/backend
COPY ./ /app/backend

# Expose port of application
EXPOSE 8191

CMD python3 /app/backend/serve.py
