FROM python:3.14-alpine AS builder

LABEL maintainer="Chaojie Yan <ushareroses@gmail.com>"

# Setup basic Linux packages
RUN apk update && \
    apk add --no-cache build-base libffi-dev make && \
    apk upgrade && \
    rm -rf /var/cache/apk/*

# Setup base folder
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    mkdir -p /services/

# Set workdir
WORKDIR /services/court-pipeline/

COPY . .

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=2.2.1 \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # no virtual env need for container
    POETRY_VIRTUALENVS_CREATE=false

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$PATH"

# install dependencies
RUN python -m pip install --no-cache --upgrade pip && \
    python -m pip install --no-cache poetry==${POETRY_VERSION} && \
    find /usr/local/ -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

# Add PYTHONPATH
ENV PYTHONPATH /services/court-pipeline/

RUN poetry install --no-cache

FROM python:3.14-alpine AS dev

COPY --from=builder /bin/ /bin/
COPY --from=builder /etc/ /etc/
COPY --from=builder /usr/ /usr/
COPY --from=builder /lib/ /lib/
COPY --from=builder --chown=usharerose:usharerose --chmod=750 /services/court-pipeline/ /services/court-pipeline/
COPY --from=builder /sbin/ /sbin/

# Set workdir
WORKDIR /services/court-pipeline/

USER root
