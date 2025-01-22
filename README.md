# Projeto Final - MATA53 Teoria dos Grafos

Projeto para otimização da colocação de câmeras de segurança no bairro da Ondina utilizando técnicas de cobertura de vértices.

## Estrutura do Projeto

O projeto está organizado nos seguintes diretórios:

- `scripts/`: Scripts Python para processamento e análise
  - `1_coleta_grafo_ondina.py`: Coleta dados do OpenStreetMap
  - `2_gera_instancia.py`: Gera grafo e calcula cobertura de vértices
  - `3_visualiza_instancia.py`: Visualiza o grafo e destaca vértices cobertos
  - `4_analisa_instancia.py`: Analisa a instância gerada
  - `5_resolve_cobertura.py`: Implementa algoritmos de cobertura completa e máxima
  - `6_visualiza_cobertura.py`: Gera visualizações das soluções
  - `7_resolve_cobertura_genetico.py`: Implementa algoritmo genético para cobertura
  - `8_visualiza_comparacao.py`: Gera visualização comparativa das três abordagens

- `instancias/`: Dados de entrada
  - `ondina.json`: Grafo do bairro de Ondina

- `resultados/`: Arquivos de saída
  - `cobertura_completa.json`: Resultado da cobertura completa
  - `cobertura_maxima.json`: Resultado da cobertura máxima
  - `ga_cobertura_ondina.json`: Resultado do algoritmo genético
  - Visualizações em PNG das soluções

## Requisitos e Instalação

1. Navegue até a pasta do projeto:
```bash
cd mata53-projeto-final
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

Execute os scripts na seguinte ordem:

1. Coleta do grafo:
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

5. Resolução da cobertura:
```bash
python scripts/5_resolve_cobertura.py
```

6. Visualização da cobertura:
```bash
python scripts/6_visualiza_cobertura.py
```

7. Resolução com algoritmo genético:
```bash
python scripts/7_resolve_cobertura_genetico.py
```

8. Visualização comparativa:
```bash
python scripts/8_visualiza_comparacao.py
```

## Algoritmos de Cobertura

### Cobertura Completa (Guloso)
- Objetivo: Encontrar o menor conjunto de vértices que cubra todo o grafo
- Resultado: 61 câmeras necessárias para cobrir todos os 182 vértices
- Média: 3,0 vértices cobertos por câmera

### Cobertura Máxima (Guloso)
- Objetivo: Maximizar a cobertura com um número limitado de câmeras
- Resultado: 40 câmeras cobrindo 153 vértices (84% do total)
- Média: 3,83 vértices cobertos por câmera

### Cobertura Máxima (Genético)
- Objetivo: Otimizar a cobertura usando algoritmo genético
- Resultado: 40 câmeras cobrindo 156 vértices (86% do total)
- Média: 3,9 vértices cobertos por câmera

## Resultados

Os resultados são salvos em arquivos JSON no diretório `resultados/`:

- `cobertura_completa.json`: Solução com cobertura total (61 câmeras)
- `cobertura_maxima.json`: Solução com 40 câmeras (algoritmo guloso)
- `ga_cobertura_ondina.json`: Solução com 40 câmeras (algoritmo genético)

Visualizações:
- `visualizacao_cobertura.png`: Comparação entre cobertura completa e máxima
- `visualizacao_comparacao.png`: Comparação das três abordagens implementadas
