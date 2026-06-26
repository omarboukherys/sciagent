FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Raise download timeout (torch can be slow)
ENV UV_HTTP_TIMEOUT=300

# Copy dependency files first (better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy the source code and README
COPY src ./src
COPY README.md ./

# Install the project itself
RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "sciagents.infrastructure.api:app", "--host", "0.0.0.0", "--port", "8000"]