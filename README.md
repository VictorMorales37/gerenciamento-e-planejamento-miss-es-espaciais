# Planejador de missões espaciais

## Configuração e execução

Instale as dependências:

```sh
pip install -r requirements.txt
```

Defina `API_KEY` no ambiente ou em um arquivo `.env` na raiz do projeto e
execute:

```sh
python main.py
```

O programa lê `API_KEY` do ambiente ou do arquivo `.env` sem exigir uma
biblioteca adicional para variáveis de ambiente. Ele carrega os corpos celestes
da API, converte cada registro em um
`CorpoCeleste` e o armazena na `TabelaHash` pelo identificador. A interface
permite listar, pesquisar e filtrar corpos, planejar missões e consultar as
métricas da tabela.

## Planejamento guloso de missão

A opção de planejamento pede o orçamento de combustível e a duração máxima.
Como a API não fornece custos de viagem nem valor científico, o programa usa
estimativas didáticas por tipo de corpo:

| Tipo | Valor científico | Combustível | Duração |
| --- | ---: | ---: | ---: |
| Planeta | 10 | 5 | 5 |
| Lua | 6 | 2 | 2 |
| Planeta anão | 7 | 4 | 4 |
| Asteroide | 4 | 1 | 2 |
| Cometa | 8 | 3 | 4 |
| Estrela | 9 | 8 | 8 |
| Outros | 3 | 3 | 3 |

Esses valores são unidades abstratas para demonstrar a otimização, não
estimativas astronômicas ou de engenharia. O critério guloso ordena destinos
pela razão `valor científico / combustível`, em ordem decrescente, com o
identificador como desempate. Adiciona um destino se ambos os limites forem
respeitados e continua avaliando os demais mesmo quando um candidato não cabe.
Cada visita é tratada como independente: não são modelados rota, combustível de
retorno, posição inicial ou tempo de trânsito.

A heurística produz uma solução viável, mas não garante o ótimo global: a
ordenação prioriza eficiência de combustível e pode deixar capacidade de tempo
mal aproveitada ou perder uma combinação de destinos com valor total maior.

## Estruturas

- `TabelaHash` (`estruturas/tabela_hash.py`) calcula índices com uma função
  polinomial de base 37 e implementa busca por identificador, inserção e atualização,
  remoção, contagem de colisões, redimensionamento e fator de carga.
- `ArvoreB` e `Trie` (`estruturas/trie.py`) são somente interfaces abstratas: declaram
  assinaturas de operações, sem implementar as estruturas.

Os campos e valores recebidos da API externa preservam os nomes originais
necessários para interpretar a resposta.
