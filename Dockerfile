# Stage 1: Build Frontend
# FROM node:20-alpine AS frontend
# WORKDIR /app/frontend
# COPY frontend/package.json frontend/package-lock.json ./
# RUN npm install
# COPY frontend/ ./
# RUN npm run build
FROM oven/bun:1-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/bun.lockb* ./
RUN bun install --frozen-lockfile
COPY frontend/ ./
RUN bun run build

# Stage 2: Build Backend
FROM golang:1.24-alpine AS backend
WORKDIR /app
COPY backend/go.mod backend/go.sum ./
RUN go mod download
COPY backend/ ./
COPY data/ ./data/
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server .

# Stage 3: Final Image
FROM alpine:latest
WORKDIR /app
COPY --from=backend /app/server .
COPY --from=frontend /app/frontend/dist ./public
COPY --from=backend /app/data ./data
EXPOSE 8080
CMD ["/app/server"]
