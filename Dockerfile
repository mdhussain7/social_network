# # OS: Ubuntu 22.04 image
# FROM ubuntu:22.04

# # Non interactive
# ENV DEBIAN_FRONTEND=noninteractive

# # Update package lists and install necessary packages
# RUN apt-get update -y && \
#     apt-get install -y --no-install-recommends \
#     build-essential \
#     libxml2-dev \
#     libldap2-dev \
#     libxslt1-dev \
#     unixodbc-dev \
#     libxmlsec1-dev \
#     libsasl2-dev \
#     libffi-dev \
#     wget \
#     xorg \
#     python3-dev \
#     python3-pip \
#     python3-venv \
#     python3-wheel \
#     ca-certificates \
#     vim \
#     gnupg \
#     poppler-utils

# RUN apt-get install -y --no-install-recommends postgresql postgresql-contrib

# # Install wkhtmltopdf
# RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
#     tar -xJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
#     cp -r wkhtmltox/* /usr/ && \
#     rm -rf wkhtml*

# # Set working directory
# WORKDIR /rest/social_networks
# RUN mkdir logs /rest/logs
# # Copy requirements and install dependencies
# COPY ./requirements.txt ./
# RUN pip3 install wheel && \
#     pip3 install --no-cache-dir -r requirements.txt

# # Copy project files
# COPY ./ /rest/social_networks

# # Django Model initial Migrate
# RUN python3 manage.py makemigrations && python3 manage.py migrate
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]



# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /social_networks

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*
#RUN apt-get install -y --no-install-recommends postgresql postgresql-contrib

# FROM mysql:8

# ENV MYSQL_ROOT_PASSWORD password
# COPY ./data.sql /docker-entrypoint-initdb.d/data.sql

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1
RUN python manage.py makemigrations && python manage.py migrate
# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
