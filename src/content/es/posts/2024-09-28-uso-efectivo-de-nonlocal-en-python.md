---
title: Uso efectivo de 'nonlocal' en Python
slug: uso-efectivo-de-nonlocal-en-python
date: 2024-09-28
summary: Aprende cuándo y cómo usar la palabra clave 'nonlocal' en Python.
language: es
topic: python
---

La palabra clave `nonlocal` en Python se utiliza en situaciones específicas dentro de funciones anidadas:

1. En funciones anidadas (una función dentro de otra).
2. Cuando necesitas modificar una variable de la función externa desde la función interna.
3. Cuando la variable a modificar no es global, sino del ámbito de la función externa.

Ejemplo:

```python
def funcion_externa():
    x = 10

    def funcion_interna():
        nonlocal x
        x = 20
        print(f"x interna: {x}")

    print(f"x antes: {x}")
    funcion_interna()
    print(f"x después: {x}")

funcion_externa()

```

Resultado:

```
x antes: 10
x interna: 20
x después: 20
```

`nonlocal x` indica que `x` en la función interna se refiere a la `x` de la función externa. Sin `nonlocal`, se crearía una nueva variable local `x` en la función interna.

Usa `nonlocal` con precaución, ya que puede complicar la legibilidad del código. Considéralo solo cuando sea realmente necesario modificar una variable de una función externa.

