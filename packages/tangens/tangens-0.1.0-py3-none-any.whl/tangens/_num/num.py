from __future__ import annotations
from typing import Any, Hashable, TypeVar

from ..dual import Dual
from .delta import (
    Delta,
    NegFn,
    OneHot,
    Grad,
    AddFn,
    MultFn,
    add_fn,
    mult_fn,
    neg_fn,
)


T = TypeVar("T", bound=Any)


class Num(Dual[T, Delta[T]]):
    def __init__(self, value: T, key: Hashable | None = None) -> None:
        delta: Delta[T]
        if key is None:
            delta = Delta.zero()
        else:
            delta = Delta.one_hot(key)
        self.delta = delta
        self.value = value

    @classmethod
    def new(cls, value: T, delta: Delta[T]) -> Num[T]:
        num = super().__new__(cls)
        num.value = value
        num.delta = delta
        return num

    def _value_and_grad(
        self,
        one: T,
        add: AddFn = add_fn,
        mult: MultFn = mult_fn,
        neg: NegFn = neg_fn,
    ) -> tuple[T, Grad[T]]:
        return self.value, self._grad(one, add, mult=mult, neg=neg)

    def _grad(
        self,
        one: T,
        add: AddFn = add_fn,
        mult: MultFn = mult_fn,
        neg: NegFn = neg_fn,
    ) -> Grad[T]:
        return self.delta.eval(one, add, mult=mult, neg=neg)

    def __mul__(self, other: Num[T]) -> Num[T]:
        a, b = self.astuple()
        c, d = other.astuple()
        return Num.new(a * c, b.scale(c).add(d.scale(a)))

    def __add__(self, other: Num[T]) -> Num[T]:
        a, b = self.astuple()
        c, d = other.astuple()
        return Num.new(a + c, b.add(d))

    def __sub__(self, other: Num[T]) -> Num[T]:
        a, b = self.astuple()
        c, d = other.astuple()
        return Num.new(a - c, b.sub(d))

    def __neg__(self) -> Num[T]:
        a, b = self.astuple()
        return Num.new(-a, b.neg())

    def __repr__(self) -> str:
        name = self.__class__.__name__
        value = repr(self.value)
        match self.delta.expression:
            case OneHot(key):
                return f"{name}({value}, key={repr(key)})"
            case _:
                return f"{name}({value})"
