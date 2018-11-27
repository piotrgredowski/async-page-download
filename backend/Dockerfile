FROM python:3.6-alpine

WORKDIR /deps

# Install dependencies
COPY requirements.txt /deps
RUN pip3 install -r requirements.txt

# Copy whole current directory
WORKDIR /app
COPY ./ /app

# Expose port of application
EXPOSE 8191

CMD sleep 5d
