ARG LMA_VERSION

FROM python:3.9-slim

ENV LEANPUB_MULTI_ACTION_VERSION 0.2.0

RUN pip install --upgrade pip

WORKDIR /app
COPY dist/leanpub_multi_action-$LEANPUB_MULTI_ACTION_VERSION-py3-none-any.whl /app

RUN pip install leanpub_multi_action-$LEANPUB_MULTI_ACTION_VERSION-py3-none-any.whl

ENTRYPOINT [ "lma" ]
