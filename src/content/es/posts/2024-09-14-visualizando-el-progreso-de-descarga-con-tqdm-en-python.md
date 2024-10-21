---
title: Visualizando el Progreso de Descarga con tqdm en Python
slug: visualizando-el-progreso-de-descarga-con-tqdm-en-python 
date: 2024-09-14
summary: Aprende a visualizar el progreso de descargas de archivos en Python usando tqdm. Este tutorial cubre la implementación básica, manejo de errores y técnicas avanzadas para mejorar la experiencia del usuario en aplicaciones CLI.
language: es
tags:
  - python
---

## Introducción

En el mundo de la programación, especialmente cuando se trabaja con descargas de archivos, es crucial proporcionar a los usuarios una indicación clara del progreso de la operación. Esto no solo mejora la experiencia del usuario, sino que también ayuda a evitar la incertidumbre sobre si el programa está funcionando correctamente. Aquí es donde entra en juego la biblioteca `tqdm` de Python.

La biblioteca `tqdm` es una herramienta poderosa y flexible que permite mostrar barras de progreso en la línea de comandos de manera sencilla y eficiente. En este tutorial, aprenderemos cómo utilizar `tqdm` para visualizar el progreso de descargas de archivos, proporcionando una experiencia más informativa y agradable para los usuarios de nuestros programas.

## Instalación

Antes de comenzar, necesitamos instalar las bibliotecas necesarias. Utilizaremos `tqdm` para la barra de progreso y `requests` para realizar las solicitudes HTTP. Puedes instalarlas utilizando pip:

```bash
pip install tqdm requests
```

## Implementación de la Función de Descarga

Ahora, vamos a crear una función `download` que descarga un archivo desde una URL dada y muestra una barra de progreso utilizando `tqdm`. Aquí está el código completo:

```python
# tqdm_download.py

import requests
from tqdm import tqdm

def download(url, dest_path):
    response = requests.get(url, stream=True, allow_redirects=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(dest_path, 'wb') as file, tqdm(
        desc=dest_path,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
```

### Explicación Detallada

Vamos a desglosar la función `download` para entender cómo funciona:

**Importación de bibliotecas**: 

```python
import requests
from tqdm import tqdm
```

Importamos `requests` para realizar la solicitud HTTP y `tqdm` para la barra de progreso.

**Definición de la función**:

```python
def download(url, dest_path):
```

La función toma dos argumentos: `url` (la URL del archivo a descargar) y `dest_path` (la ruta donde se guardará el archivo).

**Realización de la solicitud HTTP**:

```python
response = requests.get(url, stream=True, allow_redirects=True)
```

Utilizamos `requests.get()` con `stream=True` para obtener el contenido en fragmentos y `allow_redirects=True` para seguir redirecciones si las hay.

**Obtención del tamaño total del archivo**:

```python
total_size = int(response.headers.get('content-length', 0))
```

Extraemos el tamaño total del archivo del encabezado 'content-length' de la respuesta HTTP.

**Apertura del archivo de destino y configuración de tqdm**:

```python
with open(dest_path, 'wb') as file, tqdm(
   desc=dest_path,
   total=total_size,
   unit='B',
   unit_scale=True,
   unit_divisor=1024,
) as bar:
```

Abrimos el archivo de destino en modo escritura binaria y configuramos `tqdm` con varios parámetros para personalizar la barra de progreso.

**Descarga y escritura del archivo**:


```python
for data in response.iter_content(chunk_size=1024):
   size = file.write(data)
   bar.update(size)
```

Iteramos sobre el contenido de la respuesta en fragmentos de 1024 bytes, escribimos cada fragmento en el archivo y actualizamos la barra de progreso.

## Uso de la Función

Para utilizar esta función, simplemente llámala con la URL del archivo que deseas descargar y la ruta de destino:

```python
download('https://example.com/archivo.zip', 'archivo.zip')
```

Esto descargará el archivo `archivo.zip` y mostrará una barra de progreso en la línea de comandos:

```
archivo.zip:  38%|███           | 9.21M/23.9M [00:02<00:02, 5.25MB/s]
```

## Manejo de Errores

Es importante manejar posibles errores durante la descarga. Aquí hay una versión mejorada de la función que incluye manejo básico de errores:

```python
import requests
from tqdm import tqdm
from requests.exceptions import RequestException

def download(url, dest_path):
    try:
        response = requests.get(url, stream=True, allow_redirects=True)
        response.raise_for_status()  # Levanta una excepción para códigos de estado HTTP erróneos
        total_size = int(response.headers.get('content-length', 0))
        with open(dest_path, 'wb') as file, tqdm(
            desc=dest_path,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    except RequestException as e:
        print(f"Error durante la descarga: {e}")
    except IOError as e:
        print(f"Error al escribir el archivo: {e}")
```

## Ejemplos Adicionales

### Descarga de Múltiples Archivos

Para descargar múltiples archivos en paralelo y mostrar el progreso de cada uno, puedes utilizar `concurrent.futures` junto con `tqdm`:

```python
import concurrent.futures
from tqdm import tqdm

def download_multiple(urls, dest_paths):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download, url, path) for url, path in zip(urls, dest_paths)]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Total Progress"):
            future.result()

# Uso
urls = ['https://example.com/file1.zip', 'https://example.com/file2.zip']
paths = ['file1.zip', 'file2.zip']
download_multiple(urls, paths)
```

## Alternativas

Aunque `tqdm` es una excelente opción para mostrar el progreso, existen otras alternativas:

- [progress](https://github.com/verigak/progress/): Una biblioteca similar a `tqdm` con algunas características adicionales.
- [alive-progress](https://github.com/rsalmei/alive-progress): Ofrece barras de progreso animadas y personalizables.
- [rich](https://github.com/Textualize/rich): Una biblioteca para crear interfaces de línea de comandos ricas, que incluye barras de progreso.

## Rendimiento

El uso de `tqdm` tiene un impacto mínimo en el rendimiento de la descarga. La sobrecarga introducida por la actualización de la barra de progreso es ínfimo en comparación con el tiempo de descarga del archivo. Sin embargo, para archivos muy pequeños o conexiones muy rápidas, podrías notar una ligera disminución en la velocidad.

## Conclusión

La biblioteca `tqdm` proporciona una manera sencilla y efectiva de mostrar el progreso de las descargas en Python. Al incorporar barras de progreso en tus scripts de descarga, puedes mejorar significativamente la experiencia del usuario y proporcionar información valiosa sobre el estado de las operaciones de larga duración.

Te animo a experimentar con `tqdm` en tus propios proyectos `CLI`. Prueba diferentes configuraciones, personaliza el aspecto de las barras de progreso y explora cómo puedes integrarlas en aplicaciones más complejas.

## Recursos Adicionales

- [Documentación oficial de tqdm](https://github.com/tqdm/tqdm)
- [Documentación de requests](https://docs.python-requests.org/en/latest/)
- [Tutorial de Python sobre manejo de archivos](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Guía de Python sobre concurrencia](https://docs.python.org/3/library/concurrency.html)

