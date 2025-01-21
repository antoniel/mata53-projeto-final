# Projeto de Cobertura de Vértices em Ondina

Este projeto visa identificar locais ótimos para a instalação de câmeras no bairro de Ondina, Salvador, utilizando a técnica de cobertura de vértices em grafos. O objetivo é garantir que todas as ruas sejam monitoradas com o menor número possível de câmeras.

## Estrutura do Projeto

- **scripts/1_coleta_grafo_ondina.py**: Coleta dados do OpenStreetMap para o bairro de Ondina e salva o grafo em um arquivo.
- **scripts/2_gera_instancia.py**: Gera uma instância do grafo e calcula a cobertura de vértices.
- **scripts/3_visualiza_instancia.py**: Visualiza o grafo e destaca os nós que fazem parte da cobertura de vértices.
- **scripts/4_analisa_instancia.py**: Analisa a instância do grafo, fornecendo estatísticas e informações sobre a cobertura de vértices.
- **scripts/5_resolve_cobertura.py**: Implementa os algoritmos de cobertura completa e máxima para otimizar o posicionamento das câmeras.

## Requisitos e Instalação

1. Python 3.x
2. Navegue até a pasta do projeto:
```bash
cd mata53-projeto-final
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

As principais bibliotecas utilizadas são:
- networkx: Manipulação e análise de grafos
- osmnx: Coleta de dados do OpenStreetMap
- scipy: Computação científica
- matplotlib: Visualização de dados
- numpy, pandas: Processamento de dados
- geopandas, shapely: Manipulação de dados geográficos

## Como Executar

Todos os comandos devem ser executados a partir da pasta raiz do projeto:

1. Coleta do grafo:
```bash
python scripts/1_coleta_grafo_ondina.py
```

2. Geração da instância:
```bash
python scripts/2_gera_instancia.py
```

3. Visualização do grafo:
```bash
python scripts/3_visualiza_instancia.py
```

4. Análise da instância:
```bash
python scripts/4_analisa_instancia.py
```

5. Resolução da cobertura:
```bash
python scripts/5_resolve_cobertura.py
```

## Algoritmos de Cobertura

O script `5_resolve_cobertura.py` implementa dois algoritmos principais:

1. **Cobertura Completa**: Busca o número mínimo de câmeras necessário para cobrir todos os vértices do grafo. Utiliza uma abordagem gulosa que seleciona iterativamente os vértices que cobrem o maior número de vértices ainda não cobertos.

2. **Cobertura Máxima**: Dado um número limitado de câmeras (p), busca maximizar o número de vértices cobertos. Também utiliza uma abordagem gulosa, selecionando os vértices que proporcionam a maior cobertura adicional.

## Resultados

Os resultados da execução do algoritmo de cobertura são salvos no diretório `resultados/`:
- `cobertura_completa.json`: Contém a solução para cobertura completa do grafo, incluindo:
  - Lista de vértices selecionados para instalação de câmeras
  - Número total de câmeras necessárias
  - Cobertura total alcançada
  - Total de vértices no grafo

- `cobertura_maxima.json`: Contém a solução para cobertura máxima com número limitado de câmeras, incluindo:
  - Lista de vértices selecionados (limitada a p câmeras)
  - Número de câmeras utilizadas
  - Número de vértices cobertos
  - Total de vértices no grafo

## Exemplo de Resultados

Na execução com o grafo de Ondina:
- Cobertura Completa: Necessita de 80 câmeras para cobrir todos os 182 vértices
- Cobertura Máxima: Com 10 câmeras, consegue cobrir 42 vértices (23% do total)
