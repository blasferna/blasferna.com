---
title: Effective Use of 'nonlocal' in Python
slug: effective-use-of-nonlocal-in-python
date: 2024-09-28
summary: Discover when and how to use the 'nonlocal' keyword in Python
language: en
topic: python
---

The `nonlocal` keyword in Python is used in specific situations within nested functions:

1. In nested functions (a function inside another function).
2. When you need to modify a variable from the outer function within the inner function.
3. When the variable to be modified is not global, but belongs to the outer function's scope.

Example:

```python
def outer_function():
    x = 10

    def inner_function():
        nonlocal x
        x = 20
        print(f"inner x: {x}")

    print(f"x before: {x}")
    inner_function()
    print(f"x after: {x}")

outer_function()

```

Output:

```
x before: 10
inner x: 20
x after: 20

```

`nonlocal x` indicates that `x` in the inner function refers to the `x` from the outer function. Without `nonlocal`, a new local variable `x` would be created in the inner function.

Use `nonlocal` with caution, as it can complicate code readability. Consider it only when it's truly necessary to modify a variable from an outer function.

