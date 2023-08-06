from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Hashable, TypeVar, Callable

from .expression import (
    Expression,
    OneHot,
    Zero,
    Scale,
    Add,
    Neg,
)


F = TypeVar("F")
S = TypeVar("S")
AddAt = Callable[[Hashable, F, S], None]
Mult = Callable[[F, F], F]


@dataclass
class Eval(Generic[F, S]):
    real: F
    add_at: AddAt[F, S]
    mult: Mult[F]
    neg: Callable[[F], F]

    def clone(self, real: F) -> Eval[F, S]:
        """Create Eval with the same function parametrization"""
        return Eval(real, self.add_at, self.mult, self.neg)

    def __call__(self, expression: Expression) -> Callable[[S], S]:
        def callback(s: S) -> S:
            match expression:
                case OneHot(key):
                    self.add_at(key, self.real, s)

                case Scale(scalar, expr):
                    real = self.mult(self.real, scalar)
                    clone = self.clone(real)
                    clone(expr)(s)

                case Neg(expr):
                    real = self.neg(self.real)
                    clone = self.clone(real)
                    clone(expr)(s)

                case Add(left, right):
                    self(right)(self(left)(s))

                case Zero():
                    pass

                case expr:
                    raise TypeError(f"unrecognized expression: {expr}")
            return s

        return callback
