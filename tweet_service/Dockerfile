FROM python:3.11.11

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1

WORKDIR /tweet_service

COPY ./requirements.txt /tweet_service/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tweet_service/requirements.txt

COPY ./app /tweet_service/app

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
