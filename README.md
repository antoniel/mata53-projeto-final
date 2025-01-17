# Projeto de Cobertura de Vértices em Ondina

Este projeto visa identificar locais ótimos para a instalação de câmeras no bairro de Ondina, Salvador, utilizando a técnica de cobertura de vértices em grafos. O objetivo é garantir que todas as ruas sejam monitoradas com o menor número possível de câmeras.

## Estrutura do Projeto

- **scripts/1_coleta_grafo_ondina.py**: Coleta dados do OpenStreetMap para o bairro de Ondina e salva o grafo em um arquivo.
- **scripts/2_gera_instancia.py**: Gera uma instância do grafo e calcula a cobertura de vértices.
- **scripts/3_visualiza_instancia.py**: Visualiza o grafo e destaca os nós que fazem parte da cobertura de vértices.
- **scripts/4_analisa_instancia.py**: Analisa a instância do grafo, fornecendo estatísticas e informações sobre a cobertura de vértices.

## Requisitos

- Python 3.x
- Bibliotecas: osmnx, networkx, matplotlib, numpy, pandas, geopandas, shapely, tqdm
- pip install -r requirements.txt

## Como Executar

1. Execute `scripts/1_coleta_grafo_ondina.py` para coletar e salvar o grafo.
2. Execute `scripts/2_gera_instancia.py` para gerar a instância e calcular a cobertura de vértices.
3. Use `scripts/3_visualiza_instancia.py` para visualizar o grafo e a cobertura de vértices.
4. Execute `scripts/4_analisa_instancia.py` para obter uma análise detalhada da instância.

## Objetivo

O objetivo deste projeto é otimizar a instalação de câmeras de segurança em Ondina, garantindo cobertura total com o menor número de câmeras possível. A abordagem utiliza a teoria dos grafos para modelar o problema como uma cobertura de vértices, onde os vértices representam locais potenciais para câmeras e as arestas representam as ruas que precisam ser monitoradas.
