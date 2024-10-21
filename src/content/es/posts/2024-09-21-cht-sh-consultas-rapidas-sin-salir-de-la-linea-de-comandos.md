---
title: "cht.sh: Consultas Rápidas sin Salir de la Línea de Comandos"
slug: cht-sh-consultas-rapidas-sin-salir-de-la-linea-de-comandos
date: 2024-09-21
summary: Descubre cht.sh, una herramienta que te permite obtener información rápida sobre comandos de Linux y módulos de programación directamente desde tu terminal.
language: es
tags:
  - linux
---

## Introducción

Muchas veces cuando estamos trabajando en un servidor que no posee una interfaz gráfica y necesitamos alguna información adicional sobre un comando que vamos a ejecutar, por ejemplo: copiar o mover un archivo, comprimir, descargar desde internet, etc.

Podríamos recurrir a Google o directamente preguntarle a ChatGPT, ¿no? Sí, pero eso implicaría minimizar la terminal si estamos por [SSH](https://es.wikipedia.org/wiki/Secure_Shell) y abrir el navegador o simplemente no sería posible si estamos en frente del servidor.

Hoy les traigo un recurso que nos permitirá obtener una hoja de trucos (cheat sheet) de forma práctica directamente desde la terminal.

El recurso es [`cht.sh`](http://cht.sh/), que es simplemente un conjunto de páginas que retornan texto formateado para terminales y se utiliza en combinación con [`curl`](https://es.wikipedia.org/wiki/CURL).

## Requisitos

- Vamos a necesitar que el servidor tenga internet.
- Conocer el comando a utilizar.
- Tener instalado [curl](https://es.wikipedia.org/wiki/CURL), que ya viene preinstalado en la mayoría de los sistemas Linux y últimamente en las últimas versiones de Windows.

## Uso

Para utilizar [`cht.sh`](http://cht.sh/) simplemente necesitamos realizar una petición con el nombre del comando o herramienta del que queremos obtener más información y seguidamente obtendremos una guía rápida con ejemplos.

```bash
curl cht.sh/[reemplazar con el comando o herramienta deseada]

```

En el siguiente ejemplo veremos cómo obtener una guía rápida del comando `mv`:

```bash
curl cht.sh/mv

```

Esto nos mostrará una lista concisa de las opciones más comunes y ejemplos de uso del comando `mv`:

```bash
$  curl cheat.sh/mv
 cheat:mv
# To move a file from one place to another:
mv <src> <dest>

# To move a file from one place to another and automatically overwrite if the destination file exists:
# (This will override any previous -i or -n args)
mv -f <src> <dest>

# To move a file from one place to another but ask before overwriting an existing file:
# (This will override any previous -f or -n args)
mv -i <src> <dest>

# To move a file from one place to another but never overwrite anything:
# (This will override any previous -f or -i args)
mv -n <src> <dest>

# To move listed file(s) to a directory
mv -t <dest> <file>...

 tldr:mv
# mv
# Move or rename files and directories.
# More information: <https://www.gnu.org/software/coreutils/mv>.

# Rename a file or directory when the target is not an existing directory:
mv source target

# Move a file or directory into an existing directory:
mv source existing_directory

# Move multiple files into an existing directory, keeping the filenames unchanged:
mv source1 source2 source3 existing_directory

# Do not prompt for confirmation before overwriting existing files:
mv -f source target

# Prompt for confirmation before overwriting existing files, regardless of file permissions:
mv -i source target

# Do not overwrite existing files at the target:
mv -n source target

# Move files in verbose mode, showing files after they are moved:
mv -v source target

$

```

Con la información que nos ofrece es más que suficiente para completar la operación con seguridad.

Además de obtener más información sobre algunos comandos de Linux, [cht.sh](http://cht.sh/) también nos ofrece la posibilidad de acceder a documentaciones de módulos de lenguajes de programación, por ejemplo:

```bash
curl cht.sh/python/requests

```

Nos da una guía básica de cómo podemos utilizar el módulo `requests` de Python.

```bash
#  [Since v1.2.3](https://2.python-
#  requests.org/en/master/api/requests.PreparedRequest) Requests added
#  the PreparedRequest object. As per the documentation "it contains the
#  exact bytes that will be sent to the server".
#
#  One can use this to pretty print a request, like so:

 import requests

 req = requests.Request('POST','<http://stackoverflow.com>',headers={'X-Custom':'Test'},data='a=1&b=2')
 prepared = req.prepare()

 def pretty_print_POST(req):
     """
     At this point it is completely built and ready
     to be fired; it is "prepared".

     However pay attention at the formatting used in
     this function because it is programmed to be pretty
     printed and may differ from the actual request.
     """
     print('{}\\n{}\\r\\n{}\\r\\n\\r\\n{}'.format(
         '-----------START-----------',
         req.method + ' ' + req.url,
         '\\r\\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
         req.body,
     ))

 pretty_print_POST(prepared)

#  which produces:

 -----------START-----------
 POST <http://stackoverflow.com/>
 Content-Length: 7
 X-Custom: Test

 a=1&b=2

#  Then you can send the actual request with this:

 s = requests.Session()
 s.send(prepared)

#  These links are to the latest documentation available, so they might
#  change in content:
#  [Advanced - Prepared requests](https://2.python-
#  requests.org/en/master/user/advanced/id3) and [API - Lower level
#  classes](<https://2.python-requests.org/en/master/api/lower-level->
#  classes)
#
#  [AntonioHerraizS] [so/q/20658572] [cc by-sa 3.0]

```

## Conclusión

[cht.sh](http://cht.sh/) es un recurso interesante para los administradores de sistemas y desarrolladores que trabajan frecuentemente en entornos de línea de comandos. Proporciona acceso rápido y conveniente a información crucial sobre comandos de Linux y también módulos de programación, sin necesidad de salir de la terminal. Esta eficiencia no solo ahorra tiempo, sino que también mejora la productividad al permitir a los usuarios obtener la información que necesitan sin interrumpir su flujo de trabajo.
