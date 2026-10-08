from modelo.corpo_celeste import CorpoCeleste
from estruturas.tabela_dispersao import TabelaDispersao


class Repositorio:
    TIPOS_TRADUZIDOS = {
        "planeta": "planet",
        "lua": "moon",
        "planeta anão": "dwarf planet",
        "asteroide": "asteroid",
        "cometa": "comet",
        "estrela": "star",
    }

    def __init__(self, servico_api, tabela_dispersao: TabelaDispersao):
        self.servico_api = servico_api
        self.tabela_dispersao = tabela_dispersao

    @staticmethod
    def _converter_massa(massa):
        if massa is None:
            return None
        if isinstance(massa, dict):
            valor = massa.get("massValue")
            expoente = massa.get("massExponent")
            if valor is None or expoente is None:
                return None
            return float(valor) * 10 ** int(expoente)
        return float(massa)

    @staticmethod
    def _converter_numero(valor):
        if valor is None:
            return None
        return float(valor)

    @classmethod
    def _criar_corpo(cls, dados):
        identificador = dados.get("id")
        if not identificador:
            raise ValueError("A resposta da API contém um corpo sem identificador.")

        nome = dados.get("englishName") or dados.get("name") or identificador
        return CorpoCeleste(
            identificador=identificador,
            nome=nome,
            tipo=dados.get("bodyType") or "Desconhecido",
            massa=cls._converter_massa(dados.get("mass")),
            raio=cls._converter_numero(dados.get("meanRadius")),
            gravidade=cls._converter_numero(dados.get("gravity")),
            temperatura=cls._converter_numero(dados.get("avgTemp")),
            distancia_sol=cls._converter_numero(dados.get("semimajorAxis")),
        )

    def carregar_corpos(self):
        resposta = self.servico_api.obter_corpos()
        corpos = resposta.get("bodies") if isinstance(resposta, dict) else resposta
        if not isinstance(corpos, list):
            raise ValueError("A resposta da API não contém uma lista de corpos.")

        for dados in corpos:
            corpo = self._criar_corpo(dados)
            self.tabela_dispersao.inserir(corpo.identificador, corpo)
        return len(corpos)

    def buscar(self, identificador: str):
        return self.tabela_dispersao.buscar(identificador)

    def listar(self):
        return [
            elemento[1]
            for elemento in self.tabela_dispersao.tabela
            if elemento is not None
        ]

    def filtrar_por_tipo(self, tipo: str):
        tipo_normalizado = tipo.casefold()
        tipo_normalizado = self.TIPOS_TRADUZIDOS.get(
            tipo_normalizado,
            tipo_normalizado,
        )
        return [
            corpo
            for corpo in self.listar()
            if corpo.tipo.casefold() == tipo_normalizado
        ]

    def metricas_tabela_dispersao(self):
        return {
            "colisoes": self.tabela_dispersao.colisoes,
            "fator_carga": self.tabela_dispersao.fator_carga(),
            "tamanho": self.tabela_dispersao.tamanho,
            "capacidade": self.tabela_dispersao.capacidade,
        }
