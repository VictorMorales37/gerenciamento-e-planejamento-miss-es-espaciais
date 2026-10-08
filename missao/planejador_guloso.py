from collections.abc import Iterable

from missao.destino import Destino
from missao.missao import Missao


class PlanejadorGuloso:
    def planejar(
        self,
        destinos: Iterable[Destino],
        orcamento_combustivel: float,
        duracao_maxima: float,
    ) -> Missao:
        candidatos = list(destinos)
        identificadores = [destino.identificador for destino in candidatos]
        if len(set(identificadores)) != len(identificadores):
            raise ValueError("A lista de candidatos contém destinos duplicados.")

        candidatos.sort(
            key=lambda destino: (
                -destino.eficiencia,
                destino.identificador,
            )
        )
        missao = Missao(orcamento_combustivel, duracao_maxima)
        for destino in candidatos:
            missao.adicionar_destino(destino)
        return missao
