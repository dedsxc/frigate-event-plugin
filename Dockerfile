FROM python:3.12-alpine3.17@sha256:fc34b07ec97a4f288bc17083d288374a803dd59800399c76b977016c9fe5b8f2

ENV USER=user

# Install dependencies
RUN apk update && apk add --no-cache libffi-dev openssl-dev build-base


WORKDIR /app

COPY core /app
COPY requirements.txt /app

# Install python package
RUN python3 -m pip install --no-cache-dir -r requirements.txt 

# Set permission
RUN adduser -D -H -u 1000 $USER && \
    chown -R $USER:$USER /app

USER $USER

EXPOSE 8080

CMD ["python", "app.py"]