FROM node:14.15.1

WORKDIR /kuber-movies

COPY package.json .

RUN yarn install

COPY ./public/ /kuber-movies/public/ 

COPY ./src/ /kuber-movies/src/ 

CMD [ "yarn", "start"]