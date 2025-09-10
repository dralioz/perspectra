FROM python:3.11-bookworm
USER root
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt pyproject.toml ./
COPY src src
COPY models models
RUN pip install uv \
    && uv pip install -e . --system -v \
    && uv pip install -r dev-requirements.txt --system -v
EXPOSE 5000
USER 1001
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]
