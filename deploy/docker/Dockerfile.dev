FROM python:3.9-slim
LABEL maintainer "Alec Jordan <alecbjordan@gmail.com>"
WORKDIR /app

# Install Dependencies
RUN apt-get update
COPY src/requirements.txt .
# Cython needed first
RUN pip install Cython==0.29.21
RUN pip install --no-cache-dir -r requirements.txt

# Copy Application Files
COPY src/ ./src
COPY auto_app.py .
COPY .env.SAMPLE .env

# Set Entry/Command
EXPOSE 5000
CMD flask run --host=0.0.0.0
