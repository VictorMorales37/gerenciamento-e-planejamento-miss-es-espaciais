class TabelaHash:
    def __init__(self, capacidade=10):
        self.capacidade = capacidade
        self.tamanho = 0
        self.colisoes = 0
        self.tabela = [None] * capacidade

    #recebe uma chave e transforma a soma dos valores ASCII de cada caractere em um index
    def _hash(self, chave):
        valor = 0
        for char in chave:
            valor+= ord(char)
        return valor % self.capacidade

    #recebe uma chave e um valor, passa a chave pela função hash e coloca ambos no index resultante da tabela
    #aumenta o tamanho em 1
    #enquanto o index já estiver sendo usado, coloca a chave e o valor no próximo index
    def inserir(self, chave, valor):
        if self.tamanho > self.capacidade:
            raise Exception("Erro: a tabela hash está cheia.")
        
        indice = self._hash(chave)
        while self.tabela[indice] is not None:
            self.colisoes += 1
            indice = (indice + 1) % self.capacidade

        self.tabela[indice] = (chave, valor)
        self.tamanho += 1

    #salva a tabela hash antinga
    #cria uma vazia com o dobro da capacidade
    #insere cada par da tabela antiga na nova
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


    #pela função hash, procura o index onde deve começar a procurar a chave 
    #desse index em diante, enquanto nao acha um index vazio, verifica se a chave atual é a que se quer remover
    #se achar, remove e reorganiza a tabela

    def remover(self, chave):
        if self.tamanho < 1:
            raise Exception("Erro: não há valores na tabela hash.")
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

    #pega os elementos seguidos após o index removido e os reinsere
    # o objetivo é colocar as chaves em primeiro nos buckets 
    def _reorganizar(self, indice_removido):
        indice = (indice_removido + 1) % self.capacidade

        while self.tabela[indice] is not None:

            chave, valor = self.tabela[indice]

            self.tabela[indice] = None
            self.tamanho -= 1

            self.inserir(chave, valor)

            indice = (indice + 1) % self.capacidade