# Planejador de Missões Espaciais

Projeto acadêmico em Python para consultar corpos celestes da API Solar System OpenData, armazená-los em uma tabela hash implementada manualmente e demonstrar planejamento guloso de destinos sob restrições de combustível e duração.

## Funcionalidades

- Carregamento dinâmico de corpos celestes por HTTP/JSON.
- Armazenamento e busca por identificador com tabela hash própria e sondagem linear.
- Listagem e filtragem de corpos por tipo.
- Métricas de tamanho, capacidade, colisões registradas nas inserções, colisões
  presentes na disposição atual da tabela e fator de carga.
- Planejamento guloso didático com limites de combustível e duração.

## Documentação

A documentação técnica completa está em **[docs/DOCUMENTACAO.md](docs/DOCUMENTACAO.md)**. Ela inclui:

- fonte de dados, endpoints, exemplos de requisições e estrutura JSON;
- modelagem dos corpos celestes e da missão;
- representação, colisões, fator de carga e análise de complexidade da tabela hash;
- análise amortizada do redimensionamento;
- definição, critério e limitações do algoritmo guloso;
- arquitetura, execução e melhorias possíveis.

## Instalação e execução

Requisitos: Python 3.10 ou superior e acesso à internet.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export API_KEY="sua-chave"
python main.py
```

No Windows, ative o ambiente virtual com `.venv\\Scripts\\activate`. Também é possível configurar `API_KEY=sua-chave` em um arquivo `.env` na raiz. **Não publique nem versione uma chave real.**

A dependência externa está listada em `requirements.txt` (`requests`). O programa exige uma chave configurada no ambiente ou no arquivo `.env` e consulta a API durante a execução.

## Planejamento guloso: escopo e limitações

A heurística ordena os destinos pela razão `valor científico / custo de combustível`, depois adiciona os que cabem nos limites de combustível e duração. O valor científico soma massa, raio, gravidade, temperatura e distância ao Sol, cada uma dividida por uma referência da Terra ou por uma unidade astronômica, para normalizar as unidades e escalas. Campos ausentes contribuem com zero; a pontuação é heurística, não uma avaliação científica validada. Combustível e duração continuam sendo estimativas abstratas, não previsões de engenharia aeroespacial. Os custos de combustível foram ampliados para centenas de unidades e a entrada informa o mínimo necessário para visitar um destino disponível. O algoritmo respeita os limites configurados, mas não garante uma solução globalmente ótima e não calcula rotas ou transferências orbitais.

## Estruturas de dados

- `estruturas/tabela_hash.py`: implementação funcional usada para armazenar os corpos.
- `estruturas/arvore_b.py` e `estruturas/trie.py`: interfaces abstratas, sem implementação completa das estruturas.

## Fonte de dados

Solar System OpenData: https://api.le-systeme-solaire.net/

## Estrutura do projeto

```text
.
├── main.py
├── interface_terminal.py
├── requirements.txt
├── docs/
│   └── DOCUMENTACAO.md
├── estruturas/
├── modelo/
├── repositorio/
├── servicos/
└── missao/
```
