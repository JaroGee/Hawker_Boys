FROM node:20-alpine

WORKDIR /app
COPY frontend/package.json ./package.json
RUN npm install

COPY frontend ./
RUN npm run build

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]
