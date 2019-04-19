FROM node:lts-alpine as node

# install simple http server for serving static content
RUN mkdir -p /usr/src/ng-app

# make the 'app' folder the current working directory
WORKDIR /usr/src/ng-app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json /usr/src/ng-app/

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . /usr/src/ng-app

# build app for production with minification
RUN npm run build -- --prod

EXPOSE 80
FROM nginx:stable-alpine as nginx
COPY --from=node /usr/src/ng-app/dist/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
CMD [ "nginx", "-g", "daemon off;" ]