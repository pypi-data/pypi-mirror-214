# tangens
Automatic differentiation library for python

## Install

Requires python >= 3.10
```sh
pip install tangens
```

## Usage

```py
from tangens import Float

f = lambda x, y: y * x**2 + 3 * x**y + x / y

x = Float(4, 'x')
y = Float(-3, 'y')

value, grad = f(x, y).value_and_grad()
assert value == f(4, -3)

grad['x']  # df/dx
grad['y']  # df/dy
```
