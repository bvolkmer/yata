FROM node:lts-alpine as build-stage

WORKDIR /app
ENV PATH /app/node_modules/.bin:${PATH}

#RUN yarn add vue.cli@4.5

COPY package.json .
COPY yarn.lock .
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
