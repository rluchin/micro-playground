# ----- build stage -------------------------------------------------
FROM node:20-alpine AS build
WORKDIR /src

# 1. Only the manifest files first (enables better layer caching)
COPY package*.json ./

# 2. Clean install using the lock file
RUN npm install

# 3. Now copy the actual source code (node_modules is ignored)
COPY . .

# 4. Build the static site
RUN npm run build

# ----- serve stage -------------------------------------------------
FROM nginx:alpine
COPY --from=build /src/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80