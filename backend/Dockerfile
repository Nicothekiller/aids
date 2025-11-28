# Use the official Python image.
FROM python:3.13-slim

# Set the working directory.
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the dependency files.
COPY pyproject.toml uv.lock ./

# Install dependencies.
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy the rest of the application code.
COPY . .

# Generate the protobuf files.
RUN chmod +x generate-protos.sh
RUN ./generate-protos.sh

# Run the application.
CMD ["python", "main.py"]
