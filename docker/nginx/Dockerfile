FROM nginx:latest

WORKDIR /usr/share/nginx/html

COPY app/ .

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]