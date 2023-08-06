from typing import Generic, TypeVar


V = TypeVar("V")
D = TypeVar("D")


class Dual(Generic[V, D]):
    value: V
    delta: D

    def astuple(self) -> tuple[V, D]:
        return self.value, self.delta
