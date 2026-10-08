import math

from missao.destino import Destino


class Missao:
    def __init__(self, orcamento_combustivel, duracao_maxima):
        if not math.isfinite(orcamento_combustivel) or orcamento_combustivel < 0:
            raise ValueError("O orçamento de combustível deve ser finito e não negativo.")
        if not math.isfinite(duracao_maxima) or duracao_maxima < 0:
            raise ValueError("A duração máxima deve ser finita e não negativa.")

        self.orcamento_combustivel = orcamento_combustivel
        self.duracao_maxima = duracao_maxima
        self.destinos: list[Destino] = []
        self.combustivel_utilizado = 0.0
        self.duracao_utilizada = 0.0
        self.valor_cientifico_total = 0.0

    def pode_adicionar(self, destino: Destino) -> bool:
        return (
            self.combustivel_utilizado + destino.custo_combustivel
            <= self.orcamento_combustivel
            and self.duracao_utilizada + destino.duracao
            <= self.duracao_maxima
            and all(
                selecionado.identificador != destino.identificador
                for selecionado in self.destinos
            )
        )

    def adicionar_destino(self, destino: Destino) -> bool:
        if not self.pode_adicionar(destino):
            return False

        self.destinos.append(destino)
        self.combustivel_utilizado += destino.custo_combustivel
        self.duracao_utilizada += destino.duracao
        self.valor_cientifico_total += destino.valor_cientifico
        return True
