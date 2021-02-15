FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Install dependencies
RUN python -m pip install poetry
COPY ./pyproject.toml /pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy app
COPY ./src /app
# Copy .env file
COPY ./.env /

# Setup env variables for docker
ENV postgres_host="postgres"
ENV fastapi_env="production"

# Expose port 8000
EXPOSE 8000
