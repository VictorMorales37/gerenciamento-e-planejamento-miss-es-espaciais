class TabelaHash:
    def __init__(self, capacidade=10):
        if capacidade < 1:
            raise ValueError("A capacidade da tabela deve ser maior que zero.")

        self.capacidade = capacidade
        self.tamanho = 0
        self.colisoes = 0
        self.tabela = [None] * capacidade

    def _calcular_indice(self, chave):
        valor = 0
        for caractere in chave:
            valor = (valor * 31 + ord(caractere)) & 0xFFFFFFFF

        valor ^= valor >> 16
        valor = (valor * 0x7FEB352D) & 0xFFFFFFFF
        valor ^= valor >> 15
        valor = (valor * 0x846CA68B) & 0xFFFFFFFF
        valor ^= valor >> 16
        return valor % self.capacidade

    def _localizar_posicao(self, chave):
        indice = self._calcular_indice(chave)
        while self.tabela[indice] is not None:
            chave_atual, _ = self.tabela[indice]
            if chave_atual == chave:
                return indice, True
            indice = (indice + 1) % self.capacidade
        return indice, False

    def _inserir_sem_contabilizar(self, chave, valor):
        indice, existe = self._localizar_posicao(chave)
        if existe:
            self.tabela[indice] = (chave, valor)
            return

        self.tabela[indice] = (chave, valor)
        self.tamanho += 1

    def inserir(self, chave, valor):
        indice, existe = self._localizar_posicao(chave)
        if existe:
            self.tabela[indice] = (chave, valor)
            return

        if (self.tamanho + 1) / self.capacidade > 0.75:
            self._redimensionar()
            indice, _ = self._localizar_posicao(chave)

        indice_inicial = self._calcular_indice(chave)
        indice_contagem = indice_inicial
        while indice_contagem != indice:
            self.colisoes += 1
            indice_contagem = (indice_contagem + 1) % self.capacidade

        self.tabela[indice] = (chave, valor)
        self.tamanho += 1

    def buscar(self, chave):
        indice = self._calcular_indice(chave)
        indice_inicial = indice

        while self.tabela[indice] is not None:
            chave_atual, valor = self.tabela[indice]
            if chave_atual == chave:
                return valor
            indice = (indice + 1) % self.capacidade
            if indice == indice_inicial:
                break

        return None

    def _redimensionar(self):
        tabela_antiga = self.tabela
        self.capacidade *= 2
        self.tabela = [None] * self.capacidade
        self.tamanho = 0

        for elemento in tabela_antiga:
            if elemento is not None:
                chave, valor = elemento
                self._inserir_sem_contabilizar(chave, valor)

    def exibir(self):
        for indice, elemento in enumerate(self.tabela):
            print(f"{indice}: {elemento}")

    def fator_carga(self):
        return self.tamanho / self.capacidade

    def remover(self, chave):
        indice = self._calcular_indice(chave)
        indice_inicial = indice

        while self.tabela[indice] is not None:
            chave_atual, _ = self.tabela[indice]
            if chave_atual == chave:
                self.tabela[indice] = None
                self.tamanho -= 1
                self._reorganizar(indice)
                return True

            indice = (indice + 1) % self.capacidade
            if indice == indice_inicial:
                break

        return False

    def _reorganizar(self, indice_removido):
        indice = (indice_removido + 1) % self.capacidade
        while self.tabela[indice] is not None:
            chave, valor = self.tabela[indice]
            self.tabela[indice] = None
            self.tamanho -= 1
            self._inserir_sem_contabilizar(chave, valor)
            indice = (indice + 1) % self.capacidade
