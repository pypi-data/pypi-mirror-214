from __future__ import annotations
import math
from typing import Hashable

from tangens.base import Num, Delta


F = Num[float] | float
Grad = dict[Hashable, float]


class Float(Num[float]):
    def __init__(
        self,
        value: float | Num[float],
        key: Hashable | None = None,
    ) -> None:
        if isinstance(value, Num):
            assert key is None
            self.value = value.value
            self.delta = value.delta
            return
        super().__init__(value, key)

    def grad(self) -> Grad:
        return super()._grad(1.0)

    def value_and_grad(self) -> tuple[float, Grad]:
        return super()._value_and_grad(1.0)

    @classmethod
    def new(cls, value: float, delta: Delta[float]) -> Float:
        return Float(super().new(value, delta))

    def __add__(self, other: F) -> Float:
        return Float(super().__add__(Float(other)))

    def __radd__(self, other: F) -> Float:
        return Float(other) + self

    def __sub__(self, other: F) -> Float:
        return Float(super().__sub__(Float(other)))

    def __rsub__(self, other: F) -> Float:
        return Float(other) - self

    def __mul__(self, other: F) -> Float:
        return Float(super().__mul__(Float(other)))

    def __rmul__(self, other: F) -> Float:
        return Float(other) * self

    def __truediv__(self, other: F) -> Float:
        other = Float(other)
        a, b = self.astuple()
        c, d = other.astuple()
        t = 1 / c
        val = a * t
        delta = b.scale(c).sub(d.scale(a)).scale(t).scale(t)
        return Float.new(val, delta)

    def __rtruediv__(self, other: F) -> Float:
        return Float(other) / self

    def __neg__(self) -> Float:
        return Float(super().__neg__())

    def __pow__(self, p: F) -> Float:
        p = Float(p)
        a, b = self.astuple()
        c, d = p.astuple()
        t = a ** (c - 1)
        val = a * t
        delta = d.scale(val)
        if not delta.is_zero():
            delta = delta.scale(math.log(a))
        delta = delta.add(b.scale(c).scale(t))
        return Float.new(val, delta)

    def __rpow__(self, other: F) -> Float:
        return Float(other) ** self

    def sin(self) -> Float:
        val = math.sin(self.value)
        delta = self.delta
        if not delta.is_zero():
            delta = delta.scale(math.cos(self.value))
        return Float.new(val, delta)

    def cos(self) -> Float:
        val = math.cos(self.value)
        delta = self.delta
        if not delta.is_zero():
            delta = delta.scale(-math.sin(self.value))
        return Float.new(val, delta)

    def exp(self) -> Float:
        val = math.exp(self.value)
        delta = self.delta.scale(val)
        return Float.new(val, delta)

    def log(self, base: float | None = None) -> Float:
        x, d = self.astuple()
        if base is None:
            val = math.log(x)
            delta = d if d.is_zero() else d.scale(1 / x)
        elif isinstance(base, Num):
            msg = "log with variable base is not currently supported"
            raise TypeError(msg)
        else:
            val = math.log(x, base)
            delta = d if d.is_zero() else d.scale(1 / (x * math.log(base)))
        return Float.new(val, delta)

    def sqrt(self) -> Float:
        a, b = self.astuple()
        val = math.sqrt(a)
        delta = b if b.is_zero() else b.scale(1 / (2 * val))
        return Float.new(val, delta)
