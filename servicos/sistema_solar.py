import requests


class ServicoSistemaSolar:
    URL_BASE = "https://api.le-systeme-solaire.net/rest/bodies"

    def __init__(self, chave: str):
        if not chave:
            raise ValueError("A chave da API não pode estar vazia.")
        self.chave = chave
        self.cabecalhos = {"Authorization": f"Bearer {chave}"}

    def obter_corpos(self):
        resposta = requests.get(
            url=self.URL_BASE,
            headers=self.cabecalhos,
            timeout=30,
        )
        resposta.raise_for_status()
        return resposta.json()

    def obter_corpo(self, nome: str):
        resposta = requests.get(
            url=f"{self.URL_BASE}/{nome}",
            headers=self.cabecalhos,
            timeout=30,
        )
        resposta.raise_for_status()
        return resposta.json()
