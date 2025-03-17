FROM python:3.11.11-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /auth_service

COPY ./pyproject.toml /auth_service/pyproject.toml

COPY ./uv.lock /auth_service/uv.lock

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project --no-dev

COPY ./app /auth_service/app

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

ENV PATH="/auth_service/.venv/bin:$PATH"

EXPOSE 8001

CMD ["fastapi", "run", "app/main.py", "--port", "8001"]
