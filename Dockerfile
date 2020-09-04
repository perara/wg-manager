FROM node:14-alpine

COPY ./wg_dashboard_frontend /tmp/build
WORKDIR /tmp/build
RUN apk add --no-cache build-base python3-dev && \
npm install && npm install -g @angular/cli && \
rm -rf node_modules \ 
apk del build-base python3-dev
RUN ng build --configuration="production"


FROM alpine:3.12
MAINTAINER per@sysx.no
ENV IS_DOCKER True
WORKDIR /app
# Install dependencies
RUN apk add --no-cache --update wireguard-tools py3-gunicorn python3 py3-pip ip6tables

COPY wg_dashboard_backend /app
ENV LIBRARY_PATH=/lib:/usr/lib
# Install dependencies
RUN apk add --no-cache build-base python3-dev libffi-dev jpeg-dev zlib-dev && \
pip3 install uvicorn && \
pip3 install -r requirements.txt && \
apk del build-base python3-dev libffi-dev jpeg-dev zlib-dev

# Copy startup scripts
COPY docker/ ./startup
RUN chmod 700 ./startup/start.py

# Copy build files from previous step
COPY --from=0 /tmp/build/dist /app/build

ENTRYPOINT python3 startup/start.py


