---
title: Building a Docker Image for a Django Application on Raspberry Pi
slug: building-docker-image-django-application-raspberry-pi
date: 2023-12-02
summary: I installed my Django-based setlists app on Raspberry Pi 4, overcoming architecture challenges.
language: en
tags:
  - django
  - python
  - docker
  - raspberry-pi
  - linux
---

A few days ago, I decided to install my personal setlists creation application, available on [GitHub](https://github.com/blasferna/songlib), on my Raspberry Pi 4. While aware that I might face issues due to the difference in architecture for which the Docker image was built, I decided to take on this challenge to learn and understand the necessary steps to make it work.

## Initial Exploration

The first thing I did was create my `docker-compose.yml` file to easily rebuild the containers later:

```yaml
version: "3"

services:
  postgres:
    image: postgres:14.5
    ports:
      - 5432:5432
    container_name: database
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: postgres
    restart: unless-stopped

  songlib:
    image: ghcr.io/blasferna/songlib:v0.1
    container_name: songlib
    environment:
      - DEBUG=off
      - SECRET_KEY=secret
      - DB_NAME=songlib
      - DB_USER=postgres
      - DB_PASS=secret
      - DB_HOST=database
      - DB_PORT=5432
    ports:
      - 8080:80
    depends_on:
      - postgres
    restart: unless-stopped
```

The application requires a PostgreSQL database, so I also defined the `postgres` service. The database worked correctly, but the `songlib` service threw the following error:

```shell
exec /usr/bin/sh: exec format error
```

A quick search suggested that this error was due to the Docker image not being built for the `linux/arm64` architecture used by the Raspberry Pi 4.

## Docker Official Documentation

I decided to turn to the official Docker documentation, trusting that it would provide the correct steps to make a Docker image work on `linux/arm64` architectures.

In the official documentation, I found several strategies and opted for `Cross-compilation`, which is essentially compiling for multiple platforms simultaneously. This process generates binaries compatible with various architectures, including `linux/arm64`.

In the official documentation, I found the following snippet from a `Dockerfile`:

```yaml
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM golang:alpine AS build
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" > /log
```

I used the relevant part of the example:

```yaml
FROM --platform=$BUILDPLATFORM golang:alpine AS build
ARG TARGETPLATFORM
ARG BUILDPLATFORM
```

Using this portion of the example requires using `buildx` to create images from now on. Since I use GitHub Actions to build the image, I had to adapt it to use `buildx`. Locally, on my development machine, everything worked as expected.

The time came to release the project image with the modifications, and I was surprised when I tried to run the image on the Raspberry Pi: `exec /usr/bin/sh: exec format error`.

![Angry](https://github.com/blasferna/blasferna.com/assets/8385910/36a1b232-24cf-4dc6-b0d7-b98c6e6099b2)

I spent a couple of hours on the process and thought that using the official documentation would leave no room for error. I wondered, how is it possible that it works on my machine but not on the Raspberry Pi? Oh, right, my working environment runs on the `linux/amd64` architecture!

## The Solution

After several hours of debugging and extensive testing, I realized that the `Dockerfile` might contain an error. With confidence, I copied and pasted the necessary part from the official documentation. Could I have missed something in my excitement to find a solution?

The key lies in the following line:

```yaml
FROM --platform=$BUILDPLATFORM golang:alpine AS build
```

There is no way to perform `Cross-compilation` when importing the image for the architecture in which it is being built. That is, the base image will always be extended for `linux/amd64` in this case. The correct approach in my case, following the example of `golang:alpine`, would be:

```yaml
FROM --platform=$TARGETPLATFORM golang:alpine AS build
```

### Successful Implementation

Below, I detail the steps to build an image of a Django application that can run on Raspberry Pi 4. You can check the project that builds images for both `linux/amd64` and `linux/arm64` at [this link](https://github.com/blasferna/songlib).

(Note that this is not a step-by-step guide, so I have omitted some details and obvious requirements, such as Docker installation, Django project creation, explanation of what a Dockerfile is, a docker-compose, GitHub Actions, etc.)

`Dockerfile`:

```yaml
FROM --platform=$TARGETPLATFORM python:3.8.16-bullseye

ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

EXPOSE 80

RUN python manage.py collectstatic --no-input

CMD ["sh", "./runserver.sh"]
```

`runserver.sh` is not mandatory, but it's a way to automate some steps when starting the application:

```shell
python manage.py migrate
python manage.py createadminuser
gunicorn --bind :80 --workers 2 songlib.wsgi
```

`publish.yml`: This is the GitHub Action workflow that runs after creating a release. It builds and publishes the image to the GitHub registry.

```yaml
name: Publish a Docker image

on:
  release:
    types: [published]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push-image:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to the Container registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@v3
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

`docker-compose.yml`: Finally, the definition that allows launching the image on both a Raspberry Pi and any distribution using `linux/amd64`. Essentially, it is the same file presented at the beginning.

```yaml
version: "3"

services:
  postgres:
    image: postgres:14.5
    ports:
      - 5432:5432
    container_name: database
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: postgres
    restart: unless-stopped

  songlib:
    image: ghcr.io/blasferna/songlib:v0.3
    container_name: songlib
    environment:
      - DEBUG=off
      - SECRET_KEY=secret
      - DB_NAME=songlib
      - DB_USER=postgres
      - DB_PASS=secret
      - DB_HOST=database
      - DB_PORT=5432
    ports:
      - 8080:80
    depends_on:
      - postgres
    restart: unless-stopped
```