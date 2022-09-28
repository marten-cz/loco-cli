FROM python:3.7-alpine

WORKDIR /app
COPY . /opt/loco/

RUN cd /opt/loco/ && pip install -r requirements.txt

ENTRYPOINT ["python", "/opt/loco/localise/localise.py"]
