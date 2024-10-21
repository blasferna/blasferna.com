---
title: Realiza cálculos simples en tus formularios de Django utilizando django-calculation
slug: realiza-calculos-simples-en-tus-formularios-django
date: 2022-04-11
summary: Esta aplicación proporciona un widget de Django que obtiene su valor de una expresión definida en la instancia del widget.
language: es
tags:
  - django
  - python
---

Realiza cálculos simples en tus formularios de Django utilizando django-calculation.

## ¿Cómo funciona?
La aplicación ofrece una serie de widgets que te permiten especificar expresiones matemáticas y/o llamadas a funciones de JavaScript.

Un ejemplo básico sería realizar una multiplicación para calcular el precio total de un registro de ventas.

```python
amount = forms.DecimalField( 
    widget=calculation.FormulaInput('quantity*price')  
) 
```

En tiempo de ejecución, la expresión `quantity*price` se reemplaza por los valores correspondientes a los campos del mismo nombre presentes en el formulario.

Actualmente admite expresiones de tipo fórmula, así como operaciones de suma, cálculos de promedio, búsqueda del valor mínimo, valor máximo y conteo de registros.

## Motivación

Para ser honesto, soy demasiado perezoso para escribir código de JavaScript en plantillas que tienen formularios que requieren algún tipo de cálculo matemático. En un proyecto mediano o grande, la necesidad puede ser de varias cientos o miles de líneas de código.

Como no tengo la necesidad de implementar bibliotecas frontend avanzadas, como React, Vue u otras disponibles, ya que el enfoque MTV de Django se adapta bastante bien a los proyectos en los que participo. Buscando una forma de evitar escribir código de JavaScript para esas situaciones, decidí probar algo similar a lo que Salesforce ofrece con FormulaField, pero en este caso algo mucho más práctico centrado en lo que necesitaba.

Durante varios años he sido usuario de Oracle Forms 6i, que tenía algo muy práctico: indicar que el contenido de un cuadro de texto se generara a partir de la ejecución de una fórmula y algo muy interesante sucedía cuando se hacía referencia a otro cuadro de texto del mismo tipo, la ejecución respetaba la dependencia del contenido de la fórmula, es decir, se ejecutaba en cascada.

Con todo eso en mente, comencé el desarrollo.

## Proceso de desarrollo

La idea es bastante simple, en teoría, ejecutar las expresiones indicadas en la definición del campo de texto en un formulario de Django, respetando las referencias que puedan tener en otras expresiones del mismo contexto y activarlas cuando se modifiquen los campos de origen.

## Flujo funcional

Después de pensar en el flujo durante varios días, llegué a la conclusión de que podría funcionar de la siguiente manera.

1. Encontrar campos formulados:

Lo primero sería identificar los campos que contienen fórmulas, decidí realizar la búsqueda según el atributo `data-calculation`.

2. Encontrar dependencias:

Luego, encontrar todos los campos referenciados en las fórmulas, para ello tuve que recorrer todos los campos formulados y analizar cada una de las fórmulas.

3. Determinar el orden de ejecución:

Para determinar el orden de ejecución tuve que usar un algoritmo que consiste en asignar un peso a cada campo formulado basado en el número de veces que se hizo referencia a él, cuanto más veces se haga referencia, mayor será su peso y, por lo tanto, su ejecución se considerará después de los campos más livianos.

Código utilizado para calcular el peso de los campos

```javascript
function calculateWeight(obj, weight = 0) {
    weight++;
    for (let index = 0; index < obj.dependencies.length; index++) {
        let o = obj.dependencies[index];
        weight = calculateWeight(o, weight);
    }
    return weight;
}
```

Código para ordenar la ejecución

```javascript
function sortExecution() {
    for (let index = 0; index < calculatedFields.length; index++) {
        let obj = calculatedFields[index];
        obj.weight = calculateWeight(obj);
    }
    calculatedFields.sort(function (a, b) {
        return a.weight - b.weight;
    });
}
```


4. Encontrar campos de origen:

Luego, tuve que encontrar aquellos campos que ejecutarán los cálculos, es decir, los campos de origen, aquellos que, cuando se modifican, ejecutarán los cálculos en los lugares donde se han referenciado.

5. Agregar eventos:

Teniendo los campos de origen, todo lo que queda es agregar el evento que desencadenaría las ejecuciones, decidí usar el evento `blur` porque se activa después de perder el enfoque.

## Instalación

```
pip install django-calculation 
```

Agrega `calculation` en INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'calculation',
]
```

## Uso

Importa `calculation` y completa la definición.

### Ejemplo

Usando el widget `FormulaInput`

```python
from django import forms

import calculation


class TestForm(forms.Form):
    quantity = forms.DecimalField()
    price = forms.DecimalField()
    amount = forms.DecimalField(
        widget=calculation.FormulaInput('quantity*price') # <- usando una sola expresión matemática
    )
    apply_taxes = forms.BooleanField(initial=True)
    tax = forms.DecimalField(
        # usando expresiones matemáticas y funciones de JavaScript.
        widget=calculation.FormulaInput('apply_taxes ? parseFloat(amount/11).toFixed(2) : 0.0') 
    )
```

`django-calculation` funciona con archivos estáticos y, por lo tanto, es necesario incluir los medios del formulario en el archivo de la plantilla.


```django
<form method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit">
</form>
```


En acción:


![calculation](https://user-images.githubusercontent.com/8385910/142947517-49a5d6a0-6a6c-41d6-8f14-a140ad44fa1e.gif)


## Código abierto

Lo estuve usando durante varias semanas ajustando algunos detalles y después de un tiempo decidí lanzar el proyecto con la esperanza de que sea útil para otras personas, ya que para mí es muy práctico.

Para eso tuve que aplicar algunas mejoras, como incluirlo en el administrador de paquetes Python `PyPI`.

### Repercusión

No pasó mucho tiempo después del primer lanzamiento que recibí algunos correos electrónicos de usuarios que preguntaban sobre algunos detalles de la biblioteca, eso fue emocionante.

### Contribuir

Si tienes alguna idea sobre cómo mejorar la biblioteca o encontraste algún error, no dudes en abrir un issue en [https://github.com/blasferna/django-calculation/issues](https://github.com/blasferna/django-calculation/issues). 
