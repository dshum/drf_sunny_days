# pull the official docker image
FROM python:3.11.2-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# upgrade pip
RUN pip install --upgrade pip

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# copy project
COPY . .