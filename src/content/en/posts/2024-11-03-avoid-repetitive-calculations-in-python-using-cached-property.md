---
title: Avoid Repetitive Calculations in Python using cached_property
slug: avoid-repetitive-calculations-in-python-using-cached-property
date: 2024-11-03
summary: Learn how to use cached_property in Python to improve performance by avoiding repetitive calculations.
language: en
tags:
  - python
  - performance
---

Let's suppose we have a class that needs to perform some operations, such as calculations or database queries, within a custom attribute. A common approach might look like the following:

```python
import time

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def information(self):
        # Performing costly operations here
        result = self.calculate_complex_information()
        return f"Name: {self.name}, Age: {self.age}, Info: {result}"

    def calculate_complex_information(self):
        # Simulate a costly calculation or a database query
        time.sleep(2)  # Simulate a 2-second delay
        return "Calculated information"
  

if __name__ == "__main__":
    print("Starting...")
    p = Person("John", 30)
    # Takes 2 seconds to display the information
    print(p.information)
    # Takes 2 seconds again to display the information
    print(p.information)
```

However, this approach has a problem: every time we access the `information` attribute, all the costly operations will be executed again, which can be inefficient if we access this property frequently. This can lead to inefficient application performance, especially if the operation is particularly slow or if the property is accessed multiple times.

This is where the `cached_property` utility, available within Python’s standard library from version 3.8, can help.

This utility allows us to cache the result of a property, thus avoiding unnecessary repetitive calculations. It works similarly to a regular property but with the advantage that the value is calculated only once and stored for future calls. Let’s see how we can implement this in our previous example:

```python
import time
from functools import cached_property

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @cached_property
    def information(self):
        # Performing costly operations here
        result = self.calculate_complex_information()
        return f"Name: {self.name}, Age: {self.age}, Info: {result}"

    def calculate_complex_information(self):
        # Simulate a costly calculation or a database query
        time.sleep(2)  # Simulate a 2-second delay
        return "Calculated information"
  

if __name__ == "__main__":
    print("Starting...")
    p = Person("John", 30)
    # Takes 2 seconds to display the information the first time
    print(p.information)
    # Returns immediately regardless of the number of calls
    print(p.information)
    print(p.information)
```

In this modified example, we replaced the `@property` decorator with `@cached_property`. Now, when we access the `information` property for the first time, the costly calculation will be performed and the result will be stored. On subsequent calls, the cached value will be returned without needing to recalculate.
