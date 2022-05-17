FROM docker.io/library/python:3.8

WORKDIR /app

COPY ./ /app/

RUN pip install -r /app/requirements

ENTRYPOINT ["kopf", "run", "-A", "/app/operator.py"]
