from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, Hashable, TypeVar

from .eval import Eval
from .expression import Neg, Zero, OneHot, Scale, Add, Expression


T = TypeVar("T")
Grad = dict[Hashable, T]

BinaryOp = Callable[[T, T], T]
AddFn = BinaryOp[T]
MultFn = BinaryOp[T]
NegFn = Callable[[T], T]


def add_fn(x: T, y: T) -> T:
    return x + y  # type: ignore


def mult_fn(x: T, y: T) -> T:
    return x * y  # type: ignore


def neg_fn(x: T) -> T:
    return -x  # type: ignore


@dataclass
class Delta(Generic[T]):
    expression: Expression

    def add(self, other: Delta[T]) -> Delta[T]:
        match self.expression:
            case Zero():
                return other
            case _:
                if other.is_zero():
                    return self.clone()
                return Delta(Add(self.expression, other.expression))

    def scale(self, scalar: T) -> Delta[T]:
        match self.expression:
            case Zero():
                return Delta.zero()
            case _:
                return Delta(Scale(scalar, self.expression))

    def neg(self) -> Delta[T]:
        match self.expression:
            case Zero():
                return Delta.zero()
            case Neg(expr):
                return Delta(expr)
            case Scale(s, expr):
                return Delta(expr).neg().scale(s)  # type: ignore
            case _:
                return Delta(Neg(self.expression))

    def sub(self, other: Delta[T]) -> Delta[T]:
        match self.expression:
            case Zero():
                return other.neg()
            case _:
                return self.add(other.neg())

    @staticmethod
    def one_hot(key: Hashable) -> Delta[T]:
        return Delta(OneHot(key))

    @staticmethod
    def zero() -> Delta[T]:
        return Delta(Zero())

    def is_zero(self) -> bool:
        return self.expression is Zero()

    def clone(self) -> Delta[T]:
        return Delta(self.expression)

    def eval(
        self,
        one: T,
        add: AddFn[T],
        mult: MultFn[T],
        neg: NegFn[T],
    ) -> Grad[T]:
        def add_at(key: Hashable, value: T, store: Grad[T]) -> None:
            if key in store:
                store[key] = add(store[key], value)
            else:
                store[key] = value

        init = self.scale(one).expression
        evaluate = Eval(one, add_at=add_at, mult=mult, neg=neg)
        grad: Grad[T] = dict()
        return evaluate(init)(grad)
