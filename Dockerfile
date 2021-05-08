FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update && apt-get install -y gettext libgettextpo-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
