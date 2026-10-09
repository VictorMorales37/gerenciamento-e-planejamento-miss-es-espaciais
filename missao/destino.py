from dataclasses import dataclass
import math

from modelo.corpo_celeste import CorpoCeleste


_REFERENCIAS_NORMALIZACAO = {
    "massa": 5.9722e24,
    "raio": 6371.0,
    "gravidade": 9.80665,
    "temperatura": 288.15,
    "distancia_sol": 149597870.7,
}


@dataclass(frozen=True)
class Destino:
    corpo: CorpoCeleste
    valor_cientifico: float
    custo_combustivel: float
    duracao: float

    def __post_init__(self):
        if not math.isfinite(self.valor_cientifico) or self.valor_cientifico < 0:
            raise ValueError(
                "O valor científico deve ser finito e não negativo."
            )

        for nome, valor in (
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
        valor = sum(
            medida / referencia
            for medida, referencia in (
                (corpo.massa, _REFERENCIAS_NORMALIZACAO["massa"]),
                (corpo.raio, _REFERENCIAS_NORMALIZACAO["raio"]),
                (corpo.gravidade, _REFERENCIAS_NORMALIZACAO["gravidade"]),
                (corpo.temperatura, _REFERENCIAS_NORMALIZACAO["temperatura"]),
                (
                    corpo.distancia_sol,
                    _REFERENCIAS_NORMALIZACAO["distancia_sol"],
                ),
            )
            if medida is not None
        )
        estimativas_logisticas = {
            "planet": (500, 5),
            "moon": (200, 2),
            "dwarf planet": (400, 4),
            "asteroid": (100, 2),
            "comet": (300, 4),
            "star": (800, 8),
        }
        combustivel, duracao = estimativas_logisticas.get(
            corpo.tipo.casefold(),
            (300, 3),
        )
        return cls(
            corpo=corpo,
            valor_cientifico=valor,
            custo_combustivel=combustivel,
            duracao=duracao,
        )
