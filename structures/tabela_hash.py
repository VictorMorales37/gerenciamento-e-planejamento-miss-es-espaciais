class TabelaHash:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.tamanho = 0
        self.colisoes = 0
        self.tabela = [None] * capacidade

    def hash(self, chave):
        valor = 0
        for char in chave:
            valor+= ord(char)
        return valor % self.capacidade

    def inserir(self, chave, valor):
        indice = self.hash(chave)
        while self.tabela[indice] is not None:
            self.colisoes += 1
            indice = (indice + 1) % self.capacidade

        self.tabela[indice] = (chave, valor)
        self.tamanho += 1

        if self.tamanho > self.capacidade:
            raise Exception("Erro: a tabela hash está cheia.")

    def _rehash(self):
        tabela_antiga = self.tabela

        self.capacidade *= 2
        self.tabela = [None] * self.capacidade
        self.tamanho = 0

        for elemento in tabela_antiga:
            if elemento is not None:
                chave, valor = elemento
                self.inserir(chave, valor)

    def mostrar(self):
        for i, elemento in enumerate(self.tabela):
            print(f"{i}: {elemento}")

    def fator_carga(self):
        return self.tamanho / self.capacidade


    def remover(self, chave):
        indice = self._hash(chave)
        inicio = indice

        while self.tabela[indice] is not None:

            chave_atual, _ = self.tabela[indice]

            if chave_atual == chave:
                self.tabela[indice] = None
                self.tamanho -= 1

                # Reorganiza os elementos que estavam
                # depois desse elemento.
                self._reorganizar(indice)

                return True

            indice = (indice + 1) % self.capacidade

            if indice == inicio:
                break

        return False

    def _reorganizar(self, indice_removido):
        indice = (indice_removido + 1) % self.capacidade

        while self.tabela[indice] is not None:

            chave, valor = self.tabela[indice]

            # Remove temporariamente
            self.tabela[indice] = None
            self.tamanho -= 1

            # Insere novamente na posição correta
            self.inserir(chave, valor)

            indice = (indice + 1) % self.capacidade