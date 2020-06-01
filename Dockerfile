FROM python:3.6-alpine

WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt
COPY ./app/ .
RUN chmod +x /app/k8s-app
ENV PATH="/app:${PATH}"