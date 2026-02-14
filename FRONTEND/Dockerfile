# --- STAGE 1: BUILDER ---
FROM node:18-alpine AS builder
WORKDIR /app

# INSTALL LIBC6-COMPAT (REQUIRED FOR SOME DEPS)
RUN apk add --no-cache libc6-compat

COPY package*.json ./
RUN npm ci
COPY . .

# SET ENV VAR FOR BUILD TIME
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# GENERATES .next/standalone BECAUSE YOU SET output: "standalone" IN CONFIG
RUN npm run build

# --- STAGE 2: RUNNER ---
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# OPTIONAL: INSTALL SHARP FOR IMAGE OPTIMIZATION (HIGHLY RECOMMENDED)
# NEXT.JS NEEDS THIS FOR <Image /> COMPONENT RESIZING
RUN apk add --no-cache libc6-compat
# RUN npm install sharp (Uncomment if you want to force install sharp in runner)

# COPY ONLY NECESSARY FILES
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/static ./.next/static

# COPY THE STANDALONE BUILD
# THIS INCLUDES YOUR SERVER AND CONFIGURATION LOGIC
COPY --from=builder /app/.next/standalone ./

# EXPOSE PORT
EXPOSE 3000

# START NEXT.JS
CMD ["node", "server.js"]