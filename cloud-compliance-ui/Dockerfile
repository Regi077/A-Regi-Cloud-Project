# =============================================================================
#  Dockerfile -- Multi-stage build for Cloud Compliance React UI (Vite)
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - This Dockerfile builds and serves the React UI using Vite's "preview" mode.
#    - Vite preview server requires devDependencies; do NOT omit them in production image.
#    - Suited for development, staging, or internal tools—not for direct public production.
#    - If you want to serve static files via Nginx or serve, see instructions below.
# =============================================================================

# --- BUILD STAGE ---
FROM node:24 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build            # Output: /dist

# --- PRODUCTION STAGE ---
FROM node:24 AS prod
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY package*.json ./
RUN npm install              # Intentionally includes devDependencies for Vite preview server!
EXPOSE 4173
CMD ["npm", "run", "preview"]

# =============================================================================
#  NOTES:
#   - If you want a hardened production image for a public site, use Nginx or serve:
#       FROM node:24 as build
#       ...
#       RUN npm run build
#       FROM nginx:alpine
#       COPY --from=build /app/dist /usr/share/nginx/html
#       EXPOSE 80
#   - For now, this image is correct for the dev/staging/PoC purposes described.
#   - All endpoints assumed to be accessed via http://localhost:4173 in Docker.
# =============================================================================

#  END OF DOCKERFILE
# =============================================================================
