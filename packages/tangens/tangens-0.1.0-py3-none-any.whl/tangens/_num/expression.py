from __future__ import annotations
from typing import Generic, Hashable, NamedTuple, TypeVar
from dataclasses import dataclass


T = TypeVar("T")
E = TypeVar("E")
Key = Hashable


class Zero:
    _instance: Zero | None = None

    def __new__(cls) -> Zero:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "Zero()"


@dataclass
class OneHot:
    key: Hashable


@dataclass
class Scale(Generic[T, E]):
    scalar: T
    expression: E


@dataclass
class Neg(Generic[E]):
    expression: E


class Add(NamedTuple, Generic[E]):
    left: E
    right: E


Expression = Zero | OneHot | Scale | Add | Neg
