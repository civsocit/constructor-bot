FROM python:3.8-buster

RUN apt-get update && apt-get install ghostscript -y

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-dev --no-root

CMD ["poetry", "run", "bot"]
