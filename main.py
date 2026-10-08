import os
from pathlib import Path

from interface_terminal import InterfaceTerminal
from repositorio.repositorio import Repositorio
from servicos.sistema_solar import ServicoSistemaSolar
from estruturas.tabela_dispersao import TabelaDispersao


def _obter_chave_api():
    chave_api = os.getenv("API_KEY")
    if chave_api:
        return chave_api

    arquivo_ambiente = Path(__file__).with_name(".env")
    if not arquivo_ambiente.exists():
        return None

    for linha in arquivo_ambiente.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha.startswith("API_KEY="):
            valor = linha.partition("=")[2].strip()
            if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
                valor = valor[1:-1]
            return valor or None
    return None


def executar():
    chave_api = _obter_chave_api()
    if not chave_api:
        raise RuntimeError("Defina API_KEY no ambiente ou no arquivo .env.")

    servico_api = ServicoSistemaSolar(chave_api)
    repositorio = Repositorio(servico_api, TabelaDispersao())
    repositorio.carregar_corpos()
    InterfaceTerminal(repositorio).exibir_menu_principal()


if __name__ == "__main__":
    executar()
