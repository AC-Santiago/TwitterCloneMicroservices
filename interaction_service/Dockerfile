FROM python:3.11.11-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /interaction_service

COPY ./pyproject.toml /interaction_service/pyproject.toml

COPY ./uv.lock /interaction_service/uv.lock

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project --no-dev

COPY ./app /interaction_service/app

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

ENV PATH="/interaction_service/.venv/bin:$PATH"

EXPOSE 8003

CMD ["fastapi", "run", "app/main.py", "--port", "8003"]
