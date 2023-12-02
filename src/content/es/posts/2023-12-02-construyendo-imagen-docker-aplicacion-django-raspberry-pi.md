---
title: Construyendo una Imagen Docker para una Aplicación Django en Raspberry Pi
slug: construyendo-imagen-docker-aplicacion-django-raspberry-pi
date: 2023-12-02
summary: Instalé mi app de setlists hecho con Django en Raspberry Pi 4, superando desafíos de arquitectura.
language: es
topic: django
---


Hace unos días, decidí instalar mi aplicación personal para la elaboración de setlists, disponible en [GitHub](https://github.com/blasferna/songlib), en mi Raspberry Pi 4. Si bien sabía que podría enfrentar problemas debido a la diferencia en la arquitectura para la cual se construyó la imagen de Docker, decidí embarcarme en este desafío para aprender y entender los pasos correctos necesarios para que funcione.

## Exploración Inicial

Lo primero que hice fue crear mi archivo `docker-compose.yml` para reconstruir fácilmente los contenedores más adelante:

```yaml
version: "2"

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

La aplicación requiere una base de datos PostgreSQL, por lo que también definí el servicio `postgres`. La base de datos funcionó correctamente, pero el servicio `songlib` arrojó el siguiente error:

```shell
exec /usr/bin/sh: exec format error
```

Una breve búsqueda sugirió que este error se debía a que la imagen de Docker no estaba construida para la arquitectura `linux/arm64`, que es la que utiliza la Raspberry Pi 4.

## Documentación Oficial de Docker

Decidí recurrir a la documentación oficial de Docker, confiando en que proporcionaría los pasos correctos para hacer que una imagen de Docker funcione en arquitecturas `linux/arm64`.

En la documentación oficial encontré varias estrategias y opté por la `Cross-compilation`, que es básicamente compilar para varias plataformas simultáneamente. Este proceso genera binarios compatibles con diversas arquitecturas, incluyendo `linux/arm64`.

En la documentación oficial, encontré el siguiente fragmento de `Dockerfile`:

```yaml
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM golang:alpine AS build
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" > /log
```

Utilicé la parte relevante del ejemplo:

```yaml
FROM --platform=$BUILDPLATFORM golang:alpine AS build
ARG TARGETPLATFORM
ARG BUILDPLATFORM
```

Al usar esta porción del ejemplo, es necesario emplear buildx para crear las imágenes de ahora en adelante. Como utilizo GitHub Actions para construir la imagen, tuve que adaptarlo para que utilice buildx. A nivel local, en mi máquina de desarrollo, todo funcionaba según lo esperado.

Llegó el momento de lanzar una release de la imagen del proyecto con las modificaciones, y me llevé una sorpresa al levantar la imagen en la Raspberry Pi: `exec /usr/bin/sh: exec format error`.

![Angry](https://github.com/blasferna/blasferna.com/assets/8385910/36a1b232-24cf-4dc6-b0d7-b98c6e6099b2)

Invertí un par de horas en el proceso y pensé que utilizando la documentación oficial no habría margen de error. Me pregunté, ¿cómo es posible que funcione en mi máquina pero no en la Raspberry Pi? Ah, claro, ¡mi entorno de trabajo funciona con la arquitectura linux/amd64!

## La Solución

Después de varias horas de depuración y pruebas exhaustivas, me di cuenta de que el `Dockerfile` podría contener un error. Con confianza, copié y pegué la parte necesaria de la documentación oficial. ¿Podría haber omitido algo en mi emoción por encontrar una solución?

La clave radica en la siguiente línea:

```yaml
FROM --platform=$BUILDPLATFORM golang:alpine AS build
```

De ninguna manera se puede realizar una `Cross-compilation` al importar la imagen para la arquitectura en la que se está construyendo. Es decir, siempre se va a extender la imagen base, en este caso `golang:alpine`, para `linux/amd64`. Lo correcto en mi caso, siguiendo el ejemplo de `golang:alpine`, sería:

```yaml
FROM --platform=$TARGETPLATFORM golang:alpine AS build
```

### Lo Que Funcionó

A continuación, detallo los pasos para construir una imagen de una aplicación Django que pueda ejecutarse en Raspberry Pi 4. Pueden consultar el proyecto que construye imágenes tanto para `linux/amd64` como para `linux/arm64` en [este enlace](https://github.com/blasferna/songlib).

(Ten en cuenta que esto no es una guía paso a paso, por lo que he omitido algunos detalles y requisitos obvios, como la instalación de Docker, la creación de un proyecto Django, la explicación de qué es un Dockerfile, un docker-compose, GitHub Actions, etc.)

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

`runserver.sh` no es obligatorio, pero es una forma de automatizar algunos pasos al iniciar la aplicación:

```shell
python manage.py migrate
python manage.py createadminuser
gunicorn --bind :80 --workers 2 songlib.wsgi
```

`publish.yml`: Este es el flujo de trabajo de GitHub Action que se ejecuta después de crear un release. Se encarga de construir y publicar la imagen en el registro de GitHub.

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
      packages:

 write

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

`docker-compose.yml`: Por último, la definición que permite levantar la imagen tanto en una Raspberry Pi como en cualquier distribución que utilice `linux/amd64`. Básicamente, es el mismo archivo que se presentó al principio.

```yaml
version: "2"

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
