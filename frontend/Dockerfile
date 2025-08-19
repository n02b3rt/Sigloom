
# Frontend Dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f pnpm-lock.yaml ]; then npm i -g pnpm && pnpm i;     elif [ -f yarn.lock ]; then yarn install --frozen-lockfile;     elif [ -f package-lock.json ]; then npm ci; else npm i; fi
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=build /app .
EXPOSE 3000
CMD ["npm", "start"]
