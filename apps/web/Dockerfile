FROM node:20-alpine as deps
WORKDIR /app
COPY apps/web/package.json apps/web/pnpm-lock.yaml* ./
RUN corepack enable && corepack prepare pnpm@9.12.2 --activate && pnpm install --frozen-lockfile || pnpm install

FROM node:20-alpine as builder
WORKDIR /app
COPY --from=deps /root/.local/share/pnpm /root/.local/share/pnpm
COPY --from=deps /usr/local/bin/pnpm /usr/local/bin/pnpm
COPY apps/web ./
RUN pnpm build || true

FROM node:20-alpine as runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app .
EXPOSE 3000
CMD ["pnpm", "start"]
