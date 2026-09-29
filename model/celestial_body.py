class CelestialBody:
    def __init__(
        self,
        id,
        nome,
        tipo,
        massa,
        raio,
        gravidade,
        temperatura,
        distancia_sol
    ):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.massa = massa
        self.raio = raio
        self.gravidade = gravidade
        self.temperatura = temperatura
        self.distancia_sol = distancia_sol