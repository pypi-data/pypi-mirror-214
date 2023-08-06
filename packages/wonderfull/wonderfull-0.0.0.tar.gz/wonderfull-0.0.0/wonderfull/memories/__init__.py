from abc import abstractmethod
from typing import Any, Hashable, Protocol


# FIXME: Data type should not be Any.
class Memory(Protocol):
    @abstractmethod
    def save(self, key: Hashable, data: Any) -> None:
        ...

    @abstractmethod
    def retrieve(self, key: Hashable) -> Any:
        ...

    def __getitem__(self, key: Hashable) -> Any:
        return self.retrieve(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.save(key, value)
