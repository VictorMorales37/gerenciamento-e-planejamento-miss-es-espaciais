class CorpoCeleste:
    def __init__(
        self,
        identificador: str,
        nome: str,
        tipo: str,
        massa: float | None,
        raio: float | None,
        gravidade: float | None,
        temperatura: float | None,
        distancia_sol: float | None,
    ):
        self.identificador = identificador
        self.nome = nome
        self.tipo = tipo
        self.massa = massa
        self.raio = raio
        self.gravidade = gravidade
        self.temperatura = temperatura
        self.distancia_sol = distancia_sol
