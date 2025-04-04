FROM node:18 as builder
WORKDIR /app
COPY webui/ .
RUN npm install && npm run build

FROM node:18-slim
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/build ./build
CMD ["serve", "-s", "build", "-l", "3000"]
