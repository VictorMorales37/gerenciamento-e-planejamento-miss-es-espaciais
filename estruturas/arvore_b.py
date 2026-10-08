from abc import ABC, abstractmethod


class ArvoreB(ABC):
    @abstractmethod
    def inserir(self, chave: str, valor: object) -> None:
        ...

    @abstractmethod
    def buscar(self, chave: str) -> object | None:
        ...

    @abstractmethod
    def remover(self, chave: str) -> bool:
        ...

    @abstractmethod
    def em_ordem(self) -> list[tuple[str, object]]:
        ...
