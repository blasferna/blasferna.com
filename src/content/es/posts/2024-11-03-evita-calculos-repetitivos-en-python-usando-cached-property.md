---
title: Evita Cálculos Repetitivos en Python usando cached_property
slug: evita-calculos-repetitivos-en-python-usando-cached-property
date: 2024-11-03
summary: Aprende a usar cached_property en Python para mejorar el rendimiento al evitar cálculos repetitivos.
language: es
tags:
  - python
  - performance
---

Supongamos que tenemos una clase que necesita realizar algunas operaciones, como cálculos o consultas a la base de datos, dentro de un atributo personalizado. Lo común sería elaborar algo similar a lo siguiente:

```python
import time

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def information(self):
        # Aquí realizamos operaciones costosas
        result = self.calculate_complex_information()
        return f"Name: {self.name}, Age: {self.age}, Info: {result}"

    def calculate_complex_information(self):
       # Simulamos un cálculo costoso o una consulta a la base de datos
        time.sleep(2)  # Simulamos un retraso de 2 segundos
        return "Calculated information"
  

if __name__ == "__main__":
    print("Starting...")
    p = Person("John", 30)
    # Tarda 2 segundos en mostrar la información
    print(p.information)
    # Tarda 2 segundos en mostrar la información
    print(p.information)

```

Sin embargo, este enfoque tiene un problema: cada vez que accedemos al atributo `information`, se realizarán nuevamente todas las operaciones costosas, lo cual puede ser ineficiente si accedemos a esta propiedad con frecuencia. Esto puede llevar a un rendimiento poco eficiente de nuestra aplicación, especialmente si la operación es particularmente lenta o si se accede a la propiedad múltiples veces.

Allí es donde puede ayudarnos la utilidad `cached_property` que se encuentra disponible dentro de la librería estándar de Python desde la versión 3.8. 

Esta utilidad nos permite almacenar en caché el resultado de una propiedad, evitando así cálculos repetitivos innecesarios. Funciona de manera similar a una propiedad regular, pero con la ventaja de que el valor se calcula solo una vez y se almacena para futuras llamadas. Veamos cómo podemos implementar esto en nuestro ejemplo anterior:

```python
import time
from functools import cached_property

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @cached_property
    def information(self):
        # Aquí realizamos operaciones costosas
        result = self.calculate_complex_information()
        return f"Name: {self.name}, Age: {self.age}, Info: {result}"

    def calculate_complex_information(self):
       # Simulamos un cálculo costoso o una consulta a la base de datos
        time.sleep(2)  # Simulamos un retraso de 2 segundos
        return "Calculated information"
  

if __name__ == "__main__":
    print("Starting...")
    p = Person("John", 30)
    # Tarda 2 segundos en mostrar la información la primera vez
    print(p.information)
    # Retorna inmediatamente sin importar la cantidad de llamadas que reciba
    print(p.information)
    print(p.information)

```

En este ejemplo modificado, hemos reemplazado el decorador `@property` por `@cached_property`. Ahora, cuando accedamos a la propiedad `information` por primera vez, se realizará el cálculo costoso y se almacenará el resultado. En las siguientes llamadas, se devolverá el valor almacenado en caché sin necesidad de recalcular.
