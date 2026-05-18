from abc import ABC, abstractmethod


class BaseNumArgs(ABC):
    @property
    @abstractmethod
    def cardinality_repr(self) -> str: ...

    @property
    @abstractmethod
    def is_variadic(self) -> bool: ...

    @abstractmethod
    def must_stop_consumption(self, count: int, /) -> bool: ...

    @abstractmethod
    def is_valid(self, count: int, /) -> bool: ...
