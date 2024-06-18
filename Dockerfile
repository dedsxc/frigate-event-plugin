FROM python:3.11-alpine3.17@sha256:607af960065410fcfabfb7402ef4b7e8bf8e79691c63a99a2c14e7c07efa1774

ENV USER=user

# Install dependencies
RUN apk update && apk add --no-cache libffi-dev openssl-dev build-base


WORKDIR /app

COPY core /app/core
COPY requirements.txt /app

# Install python package
RUN python3 -m pip install --no-cache-dir -r requirements.txt 

# Set permission
RUN adduser -D -H -u 1000 $USER && \
    chown -R $USER:$USER /app

USER $USER

CMD ["python3", "core/app.py"]