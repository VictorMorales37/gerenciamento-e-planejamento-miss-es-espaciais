from dataclasses import dataclass
import math

from modelo.corpo_celeste import CorpoCeleste


@dataclass(frozen=True)
class Destino:
    corpo: CorpoCeleste
    valor_cientifico: float
    custo_combustivel: float
    duracao: float

    def __post_init__(self):
        for nome, valor in (
            ("valor científico", self.valor_cientifico),
            ("custo de combustível", self.custo_combustivel),
            ("duração", self.duracao),
        ):
            if not math.isfinite(valor) or valor <= 0:
                raise ValueError(f"O {nome} deve ser finito e maior que zero.")

    @property
    def identificador(self):
        return self.corpo.identificador

    @property
    def eficiencia(self):
        return self.valor_cientifico / self.custo_combustivel

    @classmethod
    def de_corpo(cls, corpo):
        estimativas = {
            "planet": (10, 5, 5),
            "moon": (6, 2, 2),
            "dwarf planet": (7, 4, 4),
            "asteroid": (4, 1, 2),
            "comet": (8, 3, 4),
            "star": (9, 8, 8),
        }
        valor, combustivel, duracao = estimativas.get(
            corpo.tipo.casefold(),
            (3, 3, 3),
        )
        return cls(
            corpo=corpo,
            valor_cientifico=valor,
            custo_combustivel=combustivel,
            duracao=duracao,
        )
