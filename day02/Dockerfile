FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install vim -y

FROM nginx:latest

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 8080 4241

CMD ["nginx", "-g", "daemon off;"]
