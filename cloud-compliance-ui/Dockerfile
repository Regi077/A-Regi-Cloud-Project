# Build stage
FROM node:24 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:24 AS prod
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY package*.json ./
RUN npm install           # <-- Do not omit dev dependencies!
EXPOSE 4173
CMD ["npm", "run", "preview"]
