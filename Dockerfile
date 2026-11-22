FROM python:3.14-slim

ARG APP_VARIANT=unknown
ARG APP_COMMIT=unknown
ARG APP_BUILD_TIME=unknown

WORKDIR /app

COPY packages/ /packages/
COPY requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check --root-user-action ignore -r requirements.txt

COPY app/ .

ENV APP_VARIANT=$APP_VARIANT \
    APP_COMMIT=$APP_COMMIT \
    APP_BUILD_TIME=$APP_BUILD_TIME \
    PYTHONUNBUFFERED=1

USER 10001
EXPOSE 8080
CMD ["python", "main.py"]
