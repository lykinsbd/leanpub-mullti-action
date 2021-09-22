FROM python:3.9-slim

ARG LMA_VERSION
ENV LMA_VERSION $LMA_VERSION
ARG WHEEL_DIR .
ENV WHEEL_DIR $WHEEL_DIR

RUN pip install --upgrade pip

WORKDIR /app
COPY $WHEEL_DIR/leanpub_multi_action-$LMA_VERSION-py3-none-any.whl /app

RUN pip install leanpub_multi_action-$LMA_VERSION-py3-none-any.whl

ENTRYPOINT [ "lma" ]
