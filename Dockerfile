FROM ubuntu:20.04
ENV TZ=Europe/Minsk
ENV DEBIAN_FRONTEND=noninteractive

#COPY ./wg-manager /tmp/build
RUN mkdir -p /tmp/build
WORKDIR /tmp/build

RUN apt-get update && apt-get install -y \
  nodejs \
  npm \
  && rm -rf /var/lib/apt/lists/*


RUN npm cache clean --force
RUN npm install
RUN npm install @angular/cli
RUN node_modules/@angular/cli/bin/ng build --configuration="production"
RUN rm -rf node_modules
RUN apt-get purge nodejs npm -y

FROM ubuntu:20.04
LABEL maintainer="per@sysx.no"
ENV IS_DOCKER True
WORKDIR /app
ENV LIBRARY_PATH=/lib:/usr/lib
ENV TZ=Europe/Oslo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY wg-manager-backend /app

# Install dependencies
#RUN apk add --no-cache --update wireguard-tools py3-gunicorn python3 py3-pip ip6tables
RUN apt-get update && apt-get install -y \
  wireguard-tools \
  iptables \
  iproute2 \
  python3 \
  python3-pip \
  python3-dev \
  python3-gunicorn \
  python3-uvicorn \
  gunicorn \
  && rm -rf /var/lib/apt/lists/*


RUN pip3 install -r requirements.txt

# Install dependencies
#RUN apk add --no-cache build-base python3-dev libffi-dev jpeg-dev zlib-dev && \
#pip3 install uvicorn && \
#pip3 install -r requirements.txt && \
#apk del build-base python3-dev libffi-dev jpeg-dev zlib-dev

# Copy startup scripts
COPY docker/ ./startup
RUN chmod 700 ./startup/start.py

# Copy build files from previous step
COPY --from=0 /tmp/build/dist /app/build

ENTRYPOINT python3 startup/start.py


