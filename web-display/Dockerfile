# run with mounted /output directory (e.g. via docker compose)
FROM node:current-alpine
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
CMD rm -rf /output/* && cp -r dist/. /output/
