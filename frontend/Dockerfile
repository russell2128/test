FROM archlinux:latest

RUN ["pacman", "--noconfirm", "-Syu"]
RUN ["pacman", "--noconfirm", "-S", "nodejs", "npm"]

WORKDIR /usr/src/app

COPY package*.json ./

RUN ["npm", "install"]

COPY . .

EXPOSE 10200

ENTRYPOINT ["npm", "start", "--", "--port", "10200"]
