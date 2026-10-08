from abc import ABC, abstractmethod


class ArvorePrefixos(ABC):
    @abstractmethod
    def inserir(self, chave: str, valor: object) -> None:
        ...

    @abstractmethod
    def buscar(self, chave: str) -> object | None:
        ...

    @abstractmethod
    def contem(self, chave: str) -> bool:
        ...

    @abstractmethod
    def contem_prefixo(self, prefixo: str) -> bool:
        ...

    @abstractmethod
    def buscar_prefixo(self, prefixo: str) -> list[tuple[str, object]]:
        ...

    @abstractmethod
    def remover(self, chave: str) -> bool:
        ...
