FROM python:3.11.11

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /bff_service

COPY ./pyproject.toml /bff_service/pyproject.toml

COPY ./uv.lock /bff_service/uv.lock

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project --no-dev

COPY ./app /bff_service/app

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

ENV PATH="/bff_service/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
