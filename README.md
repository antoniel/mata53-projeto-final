# Posicionamento Ótimo de Câmeras de Segurança em Ondina

Este projeto aborda a otimização do posicionamento de câmeras de segurança no bairro de Ondina em Salvador, utilizando conceitos e algoritmos da teoria dos grafos. O objetivo principal é desenvolver uma solução que otimize o posicionamento das câmeras de segurança modelando a região como um grafo e aplicando algoritmos de cobertura mínima de vértices.

## Estrutura do Projeto

```
.
├── scripts/
│   ├── 1_coleta_grafo_ondina.py    # Coleta dados do grafo do OpenStreetMap
│   ├── 2_gera_instancia.py         # Gera instâncias do problema
│   ├── 3_visualiza_instancia.py    # Visualiza o grafo e as instâncias
│   ├── 4_analisa_instancia.py      # Analisa as instâncias geradas
│   └── grafo_ondina.gpickle        # Dados do grafo armazenados
├── instancias/                      # Instâncias geradas
└── main.tex                         # Documentação do projeto
```

## Requisitos

- Python 3.8+
- NetworkX
- Matplotlib
- JSON
- Acesso à API do OpenStreetMap

## Configuração

1. Criar um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Unix/macOS
# ou
.\venv\Scripts\activate  # No Windows
```

2. Instalar dependências:
```bash
pip3.11 install -r requirements.txt
```

## Como Usar

O projeto é dividido em quatro scripts principais que devem ser executados em sequência:

1. **Coletar Dados do Grafo**:
```bash
python3.11 scripts/1_coleta_grafo_ondina.py
```
Este script coleta dados da rede viária do OpenStreetMap para o bairro de Ondina.

2. **Gerar Instância do Problema**:
```bash
python3.11 scripts/2_gera_instancia.py
```
Cria instâncias do problema baseadas nos dados do grafo coletados.

3. **Visualizar Instância**:
```bash
python3.11 scripts/3_visualiza_instancia.py
```
Gera uma visualização do grafo e da instância do problema.

4. **Analisar Instância**:
```bash
python3.11 scripts/4_analisa_instancia.py
```
Realiza análises nas instâncias geradas.

## Descrição do Projeto

Este projeto é parte da disciplina MATA53 - Teoria dos Grafos da Universidade Federal da Bahia. Ele aplica conceitos fundamentais da teoria dos grafos para resolver um problema real de posicionamento de câmeras de segurança no bairro de Ondina.

O problema é modelado como um problema de cobertura mínima de vértices onde:
- Os vértices representam possíveis localizações de câmeras
- As arestas representam conexões visuais ou físicas entre pontos

A solução implementa e compara diferentes algoritmos estudados na disciplina para resolver o problema de cobertura mínima, analisando sua complexidade computacional e eficiência.

## Contribuidores

- Antoniel Magalhães
- João Leahy
- Luis Felipe

## Licença

Este projeto é parte do trabalho acadêmico para a disciplina MATA53 - Teoria dos Grafos da UFBA.
