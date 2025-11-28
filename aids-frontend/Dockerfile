# Stage 1: Build the application
FROM denoland/deno:latest as builder

WORKDIR /app

# Copy all the frontend code
COPY . .

# Build the application
RUN deno install
RUN deno task build

# Stage 2: Serve the application with Nginx
FROM nginx:latest

# Copy the build output from the builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
