FROM node:14.16.1

RUN apt-get clean && apt-get update && apt-get install -yqq \
    xvfb libxtst6 libxss1 libgconf-2-4 libnss3 libasound2 libgtk2.0-0 libgtk-3-0 libnotify-dev xauth libgbm-dev

WORKDIR /app/frontend

# Install serverless for deployment
RUN npm install -g serverless@2
RUN npm install -g serverless-finch@2
RUN npm install -g serverless-build-client