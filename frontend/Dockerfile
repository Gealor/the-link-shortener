FROM node:20-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

ARG PORT=5500
ENV PORT=${PORT}

RUN npm run build

EXPOSE ${PORT}

CMD ["sh", "-c", "npx vite preview --port $PORT --host"]