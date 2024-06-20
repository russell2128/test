FROM archlinux:latest

RUN ["pacman", "--noconfirm", "-Syu"]
RUN ["pacman", "--noconfirm", "-S", "python", "python-pip"]

WORKDIR /backend-server

COPY . /backend-server

RUN ["pip", "install", "--no-cache-dir", "-r", "requirement.txt"]

EXPOSE 10400

ENV PYTHONPATH "/backend-server/"

ENTRYPOINT ["fastapi", "dev", "--reload", "--port", "10400", "./app/main.py"]
