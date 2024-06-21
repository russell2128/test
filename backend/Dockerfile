FROM python:3.12-alpine

WORKDIR /backend-server

COPY . /backend-server

RUN ["pip", "install", "--no-cache-dir", "-r", "requirement.txt"]

EXPOSE 10400

ENV PYTHONPATH "/backend-server/"

ENTRYPOINT ["fastapi", "run", "--port", "10400", "./capstone/main.py"]
