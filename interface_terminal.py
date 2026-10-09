import math

from missao.destino import Destino
from missao.planejador_guloso import PlanejadorGuloso


class InterfaceTerminal:
    TIPOS_TRADUZIDOS = {
        "planet": "Planeta",
        "moon": "Lua",
        "dwarf planet": "Planeta anão",
        "asteroid": "Asteroide",
        "comet": "Cometa",
        "star": "Estrela",
    }

    def __init__(self, repositorio):
        self.repositorio = repositorio

    def exibir_menu_principal(self):
        while True:
            print("\n=== PLANEJADOR DE MISSÕES ESPACIAIS ===")
            print("1. Listar corpos celestes")
            print("2. Buscar corpo por identificador")
            print("3. Filtrar corpos por tipo")
            print("4. Planejar missão")
            print("5. Consultar métricas da tabela hash")
            print("0. Sair")
            escolha = input("Escolha: ").strip()

            match escolha:
                case "1":
                    self.listar_corpos()
                case "2":
                    self.buscar_corpo()
                case "3":
                    self.filtrar_corpos()
                case "4":
                    self.planejar_missao()
                case "5":
                    self.exibir_metricas()
                case "0":
                    return
                case _:
                    print("Opção inválida.")

    @classmethod
    def _nome_tipo(cls, tipo):
        return cls.TIPOS_TRADUZIDOS.get(tipo.casefold(), tipo)

    @classmethod
    def exibir_corpo(cls, corpo):
        print(f"Identificador: {corpo.identificador}")
        print(f"Nome: {corpo.nome}")
        print(f"Tipo: {cls._nome_tipo(corpo.tipo)}")
        print(f"Massa (kg): {corpo.massa}")
        print(f"Raio médio (km): {corpo.raio}")
        print(f"Gravidade (m/s²): {corpo.gravidade}")
        print(f"Temperatura média (K): {corpo.temperatura}")
        print(f"Distância orbital (km): {corpo.distancia_sol}")

    def listar_corpos(self):
        corpos = sorted(
            self.repositorio.listar(),
            key=lambda corpo: corpo.identificador,
        )
        for corpo in corpos:
            print(
                f"{corpo.identificador}: {corpo.nome} "
                f"({self._nome_tipo(corpo.tipo)})"
            )

    def buscar_corpo(self):
        identificador = input("Identificador do corpo: ").strip()
        corpo = self.repositorio.buscar(identificador)
        if corpo is None:
            print("Corpo celeste não encontrado.")
            return
        self.exibir_corpo(corpo)

    def filtrar_corpos(self):
        tipos_disponiveis = sorted(
            {corpo.tipo for corpo in self.repositorio.listar()},
            key=lambda tipo: self._nome_tipo(tipo).casefold(),
        )
        if tipos_disponiveis:
            tipos_formatados = ", ".join(
                self._nome_tipo(tipo) for tipo in tipos_disponiveis
            )
            print(f"Tipos disponíveis: {tipos_formatados}")
        else:
            print("Nenhum tipo disponível para filtrar.")

        tipo = input("Tipo do corpo: ").strip()
        corpos = self.repositorio.filtrar_por_tipo(tipo)
        if not corpos:
            print("Nenhum corpo encontrado para esse tipo.")
            return
        for corpo in sorted(corpos, key=lambda item: item.identificador):
            print(
                f"{corpo.identificador}: {corpo.nome} "
                f"({self._nome_tipo(corpo.tipo)})"
            )

    @staticmethod
    def _ler_limite(mensagem):
        while True:
            try:
                valor = float(input(mensagem).strip())
            except ValueError:
                print("Digite um número válido.")
                continue
            if not math.isfinite(valor) or valor < 0:
                print("Digite um número finito e não negativo.")
                continue
            return valor

    def planejar_missao(self):
        destinos = [
            Destino.de_corpo(corpo)
            for corpo in self.repositorio.listar()
        ]
        minimo_combustivel = min(
            (destino.custo_combustivel for destino in destinos),
            default=None,
        )
        if minimo_combustivel is None:
            detalhe_minimo = "nenhum destino disponível"
        else:
            detalhe_minimo = (
                f"mínimo individual: {minimo_combustivel:g}"
            )

        combustivel = self._ler_limite(
            f"Orçamento de combustível ({detalhe_minimo} unidades): "
        )
        duracao = self._ler_limite("Duração máxima (unidades): ")
        missao = PlanejadorGuloso().planejar(destinos, combustivel, duracao)

        if not missao.destinos:
            print("Nenhum destino cabe nos recursos informados.")
            return

        print("\nDestinos selecionados (ordem gulosa):")
        for destino in missao.destinos:
            print(
                f"{destino.identificador}: {destino.corpo.nome} | "
                f"valor {destino.valor_cientifico:g} | "
                f"combustível {destino.custo_combustivel:g} | "
                f"duração {destino.duracao:g} | "
                f"eficiência {destino.eficiencia:.2f}"
            )
        print(f"Valor científico total: {missao.valor_cientifico_total:g}")
        print(
            f"Combustível utilizado: {missao.combustivel_utilizado:g}/"
            f"{missao.orcamento_combustivel:g}"
        )
        print(
            f"Duração utilizada: {missao.duracao_utilizada:g}/"
            f"{missao.duracao_maxima:g}"
        )

    def exibir_metricas(self):
        metricas = self.repositorio.metricas_tabela_hash()
        print(f"Corpos armazenados: {metricas['tamanho']}")
        print(f"Capacidade: {metricas['capacidade']}")
        print(f"Colisões registradas em inserções: {metricas['colisoes']}")
        print(
            "Colisões atuais (elementos deslocados): "
            f"{metricas['colisoes_atuais']}"
        )
        print(f"Fator de carga: {metricas['fator_carga']:.2f}")
