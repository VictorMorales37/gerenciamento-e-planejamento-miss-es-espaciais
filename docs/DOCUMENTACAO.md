# Documentação técnica — Planejador de Missões Espaciais

**Projeto acadêmico — Grupo 9**  
**Integrante:** Victor Matheus Marques Morales
**Matrícula:** 25100782
**Linguagem:** Python  
**Data desta documentação:** 08/10/2026

## 1. Objetivo

O projeto consulta dados de corpos celestes por uma API HTTP, converte os registros para objetos Python e mantém os objetos em uma tabela hash implementada pelo próprio projeto. Pela interface de terminal, é possível listar corpos, buscar por identificador, filtrar por tipo, consultar métricas da tabela e montar uma seleção de destinos com uma heurística gulosa.

O planejador é um modelo didático de alocação de recursos. Não calcula trajetórias orbitais nem representa uma simulação física de viagens espaciais.

## 2. Tecnologias e execução

- Python 3.10 ou superior (o código usa anotações de tipo como `float | None` e instruções `match`).
- Biblioteca externa: `requests`.
- Fonte de dados: Solar System OpenData, API REST.

### Instalação

Na raiz do repositório:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No Windows, ative o ambiente virtual com `.venv\\Scripts\\activate`.

O programa procura `API_KEY` primeiro nas variáveis de ambiente e depois em um arquivo `.env` na raiz. O arquivo pode conter:

```dotenv
API_KEY=sua_chave
```

Não versione uma chave real. O arquivo `.env` deve permanecer fora do Git.

Execute:

```bash
python main.py
```

O programa encerra com uma mensagem de erro se não encontrar a chave. A consulta HTTP tem timeout de 30 segundos e erros HTTP são propagados por `raise_for_status()`.

## 3. Organização do código

```text
.
├── main.py
├── interface_terminal.py
├── requirements.txt
├── estruturas/
│   ├── tabela_hash.py
│   ├── arvore_b.py
│   └── trie.py
├── modelo/
│   └── corpo_celeste.py
├── repositorio/
│   └── repositorio.py
├── servicos/
│   └── sistema_solar.py
└── missao/
    ├── destino.py
    ├── missao.py
    └── planejador_guloso.py
```

- **`main.py`:** obtém a chave de API, instancia os componentes, carrega os corpos e inicia a interface.
- **`servicos/sistema_solar.py`:** executa as requisições HTTP e converte as respostas JSON em estruturas Python.
- **`modelo/corpo_celeste.py`:** representa um corpo com identificador, nome, tipo, massa, raio, gravidade, temperatura e distância orbital.
- **`repositorio/repositorio.py`:** transforma os registros da API em objetos de domínio e oferece listagem, busca, filtro e acesso às métricas.
- **`estruturas/tabela_hash.py`:** estrutura de dados implementada no projeto e usada para armazenar os corpos.
- **`missao/destino.py`:** associa a cada corpo os valores didáticos de mérito científico, combustível e duração.
- **`missao/missao.py`:** valida os limites de recursos e acumula os destinos selecionados.
- **`missao/planejador_guloso.py`:** ordena os candidatos pela eficiência e tenta incluí-los na missão.
- **`interface_terminal.py`:** oferece o menu interativo.

## 4. API e aquisição de dados

### Fonte

- **Nome:** Solar System OpenData.
- **URL-base usada pelo código:** `https://api.le-systeme-solaire.net/rest/bodies`
- **Formato:** JSON.
- **Método HTTP:** GET.
- **Autenticação implementada:** o cliente envia `Authorization: Bearer <API_KEY>`. É necessário usar uma chave aceita pelo serviço conforme a configuração atual da API.
- **Timeout configurado:** 30 segundos.

### Endpoints implementados

| Método | Endpoint | Uso no projeto |
|---|---|---|
| GET | `https://api.le-systeme-solaire.net/rest/bodies` | Carrega a coleção de corpos na inicialização. |
| GET | `https://api.le-systeme-solaire.net/rest/bodies/{id}` | Método de serviço para consultar um corpo específico; não é usado pelo fluxo principal da interface atualmente. |

Exemplo de chamada equivalente à implementada pelo cliente:

```bash
curl -H "Authorization: Bearer SUA_CHAVE" \
  "https://api.le-systeme-solaire.net/rest/bodies"
```

A chamada de consulta individual segue o mesmo cabeçalho:

```bash
curl -H "Authorization: Bearer SUA_CHAVE" \
  "https://api.le-systeme-solaire.net/rest/bodies/mars"
```

Esses comandos documentam o formato da requisição construída pelo código; não representam uma resposta testada nesta documentação. A disponibilidade, os requisitos de autenticação e o conteúdo da API podem mudar.

### Formato JSON esperado

O repositório aceita uma resposta que seja uma lista de registros ou um objeto JSON com a lista no campo `bodies`. Para cada registro, o conversor utiliza os seguintes campos:

| Campo de origem | Atributo do modelo | Conversão |
|---|---|---|
| `id` | `identificador` | Obrigatório; registro sem identificador gera erro. |
| `englishName` (ou `name`) | `nome` | Usa o nome alternativo se o primeiro estiver ausente. |
| `bodyType` | `tipo` | Texto; usa “Desconhecido” se ausente. |
| `mass` | `massa` | Se for objeto, calcula `massValue × 10 ** massExponent`. |
| `meanRadius` | `raio` | Converte para `float`. |
| `gravity` | `gravidade` | Converte para `float`. |
| `avgTemp` | `temperatura` | Converte para `float`. |
| `semimajorAxis` | `distancia_sol` | Converte para `float`. |

Campos numéricos ausentes ou nulos são representados por `None`. A conversão da massa depende do formato de massa retornado pela API. O repositório não mantém um arquivo de dados local: a carga é feita dinamicamente por uma requisição HTTP durante a execução.

**Data de referência da documentação:** 08/10/2026. A data indica quando este documento foi preparado a partir do código do repositório, não uma validação ao vivo de todos os endpoints.

## 5. Tabela hash

A classe `TabelaHash` é a estrutura principal efetivamente implementada e usada para armazenar os corpos celestes.

### Representação e operações

- A tabela começa com capacidade 10 por padrão.
- Cada posição contém `None` ou um par `(chave, valor)`.
- A chave usada pelo repositório é o identificador do corpo celeste.
- A função de dispersão acumula os caracteres em base 31, mistura os bits do resultado e aplica módulo pela capacidade.
- A colisão é resolvida por **endereçamento aberto com sondagem linear**: após uma posição ocupada, a busca continua na próxima posição, com retorno circular ao início.
- Ao inserir uma nova chave, a tabela é redimensionada para o dobro da capacidade se a carga resultante ultrapassar 0,75.
- A remoção limpa a posição e reorganiza os elementos subsequentes do agrupamento para que continuem encontráveis.
- A interface exibe tamanho, capacidade, colisões contabilizadas e fator de carga.

O fator de carga é:

```text
fator de carga = quantidade de elementos / capacidade da tabela
```

A contagem de colisões contabiliza posições ocupadas atravessadas durante inserções comuns. Os elementos movidos durante o redimensionamento e a reorganização após remoção são reinseridos sem incrementar esse contador. Portanto, a métrica descreve as colisões registradas pelo mecanismo de inserção, não o número total de sondagens de todas as operações.

### Complexidade

Considere `n` elementos armazenados e `k` caracteres na chave.

| Operação | Caso médio esperado | Pior caso |
|---|---:|---:|
| Calcular índice hash | O(k) | O(k) |
| Buscar por chave | O(k) | O(n + k) |
| Inserir/atualizar | O(k) amortizado para inserções novas; atualização depende da sondagem | O(n + k), além do custo de redimensionamento |
| Remover | O(n + k) no pior caso, pois pode precisar localizar e reorganizar um agrupamento | O(n + k) |
| Listar todos os corpos | O(n) | O(n) |
| Filtrar por tipo | O(n) | O(n) |
| Consultar fator de carga | O(1) | O(1) |
| Redimensionar e rehash | — | O(n) reinserções, além do custo de calcular as chaves |

O caso médio da tabela hash pressupõe uma distribuição razoável das chaves e um fator de carga controlado. A sondagem linear pode formar agrupamentos; por isso, a busca e a inserção podem percorrer muitas posições e chegar a O(n) no pior caso. O cálculo do hash também percorre a string da chave, daí o termo O(k).

### Análise amortizada do redimensionamento

Uma inserção isolada que dispara o redimensionamento custa O(n), pois cria um vetor maior e reinsere os elementos existentes. Porém, a capacidade dobra geometricamente: depois de um redimensionamento, muitas inserções podem ocorrer antes do próximo. Ao longo de uma sequência de inserções, o total de elementos movidos pelos redimensionamentos é limitado por uma soma geométrica proporcional ao número de inserções. Assim, o custo adicional de redimensionar é O(1) amortizado por inserção, sob o crescimento geométrico usado pelo projeto.

Isso não significa que cada inserção seja O(1) no pior caso: uma operação individual ainda pode custar O(n), por colisões ou por redimensionamento. A análise amortizada descreve o custo médio por operação ao longo de uma sequência, não uma garantia para cada chamada.

## 6. Planejamento guloso de missões — Opção A: logística

### Problema modelado

A entrada do planejador é a lista de corpos celestes carregada pela API e dois limites fornecidos pelo usuário:

1. orçamento máximo de combustível;
2. duração máxima da missão.

Cada corpo é convertido em um candidato `Destino` com três valores didáticos: valor científico, custo de combustível e duração. O objetivo é selecionar destinos sem ultrapassar nenhum dos dois recursos e maximizar, de forma heurística, o valor científico total.

### Estimativas usadas

A API consultada não fornece os custos de missão usados pelo algoritmo. Por isso, o projeto atribui valores abstratos por tipo de corpo:

| Tipo recebido | Valor científico | Combustível | Duração |
|---|---:|---:|---:|
| Planeta (`planet`) | 10 | 5 | 5 |
| Lua (`moon`) | 6 | 2 | 2 |
| Planeta anão (`dwarf planet`) | 7 | 4 | 4 |
| Asteroide (`asteroid`) | 4 | 1 | 2 |
| Cometa (`comet`) | 8 | 3 | 4 |
| Estrela (`star`) | 9 | 8 | 8 |
| Outro tipo | 3 | 3 | 3 |

Os valores são unidades abstratas para fins acadêmicos. Não são medições reais, custos de combustível de uma espaçonave ou estimativas de duração de uma viagem.

### Critério de escolha

O planejador calcula para cada destino:

```text
eficiência = valor científico / custo de combustível
```

Os candidatos são ordenados por eficiência decrescente; em caso de empate, o identificador em ordem crescente é usado para tornar o resultado determinístico. Em seguida, cada destino é considerado nessa ordem. Ele é adicionado apenas se houver combustível e duração suficientes e se seu identificador ainda não tiver sido selecionado. Um candidato que não cabe é ignorado, e o algoritmo continua testando os demais.

### Por que uma heurística gulosa?

O critério privilegia o valor científico por unidade de combustível, é simples de explicar e permite produzir uma seleção rapidamente. A verificação de duração e combustível garante que a missão produzida respeite os dois limites.

A escolha não garante o ótimo global. O algoritmo prioriza a eficiência de combustível, mas a duração também limita a seleção; uma combinação de destinos com eficiência individual menor pode gerar valor total maior. Como exemplo didático, um destino de valor 10, combustível 5 e duração 5 tem eficiência 2; dois destinos de valor 6, combustível 2 e duração 2 têm eficiência 3 cada e podem ser preferíveis se ambos couberem, mas outras combinações de recursos podem inverter a decisão. Além disso, o modelo não considera dependência entre destinos, distâncias, rota, posição inicial, combustível de retorno nem janelas de lançamento.

### Complexidade do planejador

Considere `m` candidatos à missão.

- Converter o iterável para lista: O(m).
- Verificar identificadores duplicados usando um conjunto: O(m) esperado.
- Ordenar por eficiência: O(m log m).
- Tentar adicionar todos os candidatos: O(m²) no pior caso, porque `Missao.pode_adicionar` verifica os destinos já selecionados para impedir identificadores repetidos.
- Espaço auxiliar: O(m), para a lista de candidatos e a lista de identificadores/conjunto usados na validação.

Portanto, a complexidade total é O(m²) no pior caso, dominada pela verificação de duplicidade durante as inclusões. O custo da ordenação é O(m log m), mas não domina o limite quadrático atual.

## 7. Funcionalidades disponíveis na interface

1. **Listar corpos celestes:** apresenta identificador, nome e tipo, ordenados pelo identificador.
2. **Buscar por identificador:** consulta a tabela hash e exibe os atributos disponíveis.
3. **Filtrar por tipo:** percorre os registros armazenados e compara o tipo normalizado.
4. **Planejar missão:** solicita os limites de combustível e duração, executa a heurística gulosa e apresenta destinos e totais.
5. **Consultar métricas:** mostra tamanho, capacidade, colisões registradas e fator de carga.
6. **Sair:** encerra o menu.

A busca por identificador é a operação diretamente apoiada pela tabela hash. Listagem e filtragem percorrem os elementos armazenados.

## 8. Estruturas previstas, mas não implementadas

Os arquivos `estruturas/arvore_b.py` e `estruturas/trie.py` declaram interfaces abstratas para operações de árvore B e trie. Eles não contêm a lógica de inserção, busca ou remoção dessas estruturas e não são usados como armazenamento principal. A estrutura concreta implementada e integrada ao fluxo do programa é a tabela hash.

## 9. Limitações e possíveis melhorias

- Validar a autenticação e a disponibilidade da API no ambiente de execução, sem registrar a chave em logs.
- Adicionar testes automatizados para colisões, redimensionamento, remoção, respostas incompletas e limites da missão.
- Separar a métrica de colisões de carga das métricas de busca, remoção e rehash para tornar as medições comparáveis.
- Permitir pesquisar atributos além do tipo, caso isso seja necessário para a avaliação.
- Melhorar o custo de verificação de destinos duplicados em `Missao` mantendo um conjunto de identificadores selecionados.
- Se o escopo exigir realismo orbital, substituir as estimativas abstratas por um modelo físico validado e dados de transferência, mantendo explícitas as hipóteses.
- Implementar as estruturas abstratas apenas se forem necessárias ao escopo do trabalho; no estado atual, elas são contratos de interface, não implementações funcionais.

## 10. Integrante

**Grupo 9 — individual**

- Victor Morales — desenvolvimento, implementação e documentação do projeto.
