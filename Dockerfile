FROM node

COPY ./wg_dashboard_frontend /tmp/build
WORKDIR /tmp/build
RUN npm install && npm install -g @angular/cli
RUN ng build --configuration="production"




FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8
ENV IS_DOCKER True
RUN apk add --no-cache build-base libffi-dev

RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories
RUN apk update && apk add --no-cache wireguard-tools
COPY ./wg_dashboard_backend /app
RUN pip install -r /app/requirements.txt
COPY --from=0 /tmp/build/dist /app/build

