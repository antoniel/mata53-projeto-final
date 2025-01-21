# Projeto Final - MATA53 Teoria dos Grafos

## Problema de Colocação Ótima de Câmeras de Segurança no bairro da Ondina

Este projeto implementa diferentes algoritmos para resolver o problema de cobertura de vértices aplicado à colocação de câmeras de segurança no bairro de Ondina, Salvador.

## Estrutura do Projeto

- **scripts/1_coleta_grafo_ondina.py**: Coleta dados do OpenStreetMap para o bairro de Ondina e salva o grafo em um arquivo.
- **scripts/2_gera_instancia.py**: Gera uma instância do grafo e calcula a cobertura de vértices.
- **scripts/3_visualiza_instancia.py**: Visualiza o grafo e destaca os nós que fazem parte da cobertura de vértices.
- **scripts/4_analisa_instancia.py**: Analisa a instância do grafo, fornecendo estatísticas e informações sobre a cobertura de vértices.
- **scripts/5_resolve_cobertura.py**: Implementa os algoritmos de cobertura completa e máxima para otimizar o posicionamento das câmeras.
- **scripts/6_visualiza_cobertura.py**: Gera visualizações comparativas das soluções de cobertura completa e máxima, destacando o posicionamento das câmeras e os vértices cobertos.
- **scripts/7_resolve_cobertura_genetico.py**: Implementa um algoritmo genético para otimizar a cobertura.
- **scripts/8_visualiza_comparacao.py**: Gera visualizações comparativas das três abordagens.

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

Execute os scripts na seguinte ordem:

1. Coleta do grafo de Ondina:
```bash
python scripts/1_coleta_grafo_ondina.py
```

2. Geração da instância:
```bash
python scripts/2_gera_instancia.py
```

3. Visualização da instância:
```bash
python scripts/3_visualiza_instancia.py
```

4. Análise da instância:
```bash
python scripts/4_analisa_instancia.py
```

5. Resolução do problema de cobertura:
```bash
python scripts/5_resolve_cobertura.py
```

6. Resolução usando algoritmo genético:
```bash
python scripts/7_resolve_cobertura_genetico.py
```

7. Visualização comparativa das soluções:
```bash
python scripts/8_visualiza_comparacao.py
```

## Algoritmos de Cobertura

### Cobertura Completa (Guloso)
- Implementa um algoritmo guloso que busca cobrir todos os vértices do grafo
- Seleciona iterativamente os vértices que cobrem o maior número de vértices ainda não cobertos
- Resultado: 61 câmeras para cobrir todos os 182 vértices
- Média de 3,0 vértices cobertos por câmera

### Cobertura Máxima (Guloso)
- Implementa um algoritmo guloso com limite de câmeras
- Busca maximizar a cobertura usando no máximo 40 câmeras
- Resultado: 142 vértices cobertos (78% do total)
- Média de 3,55 vértices cobertos por câmera

### Cobertura Máxima (Genético)
- Implementa um algoritmo genético para otimizar a cobertura
- Usa população de 100 indivíduos e 200 gerações
- Resultado: 156 vértices cobertos (85% do total) com 40 câmeras
- Média de 3,9 vértices cobertos por câmera

## Resultados

Os resultados são salvos em arquivos JSON na pasta `resultados/`:
- `cobertura_completa.json`: Solução de cobertura completa
- `cobertura_maxima.json`: Solução de cobertura máxima com algoritmo guloso
- `ga_cobertura_ondina.json`: Solução de cobertura máxima com algoritmo genético

Visualizações são geradas em:
- `resultados/visualizacao_cobertura.png`: Comparação das soluções gulosas
- `resultados/visualizacao_comparacao.png`: Comparação das três abordagens
