FROM python:alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN  python3 -m pip install --upgrade pip --no-cache-dir \
    && python3 -m pip install -r requirements.txt --no-cache-dir

COPY docker-entrypoint.sh /usr/bin/docker-entrypoint.sh

COPY . /app

VOLUME ["/data"]

EXPOSE 5555

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]