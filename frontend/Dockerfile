# Stage 0, "build-stage", based on Bun, to build and compile the frontend
FROM oven/bun:1 AS build-stage

WORKDIR /app

COPY package.json bun.lock /app/

COPY package.json .

WORKDIR /app/frontend

RUN bun install

COPY . .

CMD ["sh", "-c", "bun run build-only && cp -rt /output dist/*"]
