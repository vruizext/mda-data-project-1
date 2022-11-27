FROM python:3.9-slim
RUN mkdir generador
COPY src generador
WORKDIR "generador"
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]