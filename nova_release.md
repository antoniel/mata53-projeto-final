# Nova Release: Implementação do TSP com Coleta de Bônus e Passageiros (TSP-BC-PP)

## Visão Geral das Mudanças
Esta release adapta o projeto para resolver o Problema do Caixeiro Viajante com Coleta de Bônus e Passageiros (TSP-BC-PP) no bairro de Ondina. As alterações incluem a coleta de pontos de interesse, pontos de ônibus e a adição de parâmetros específicos do problema.

## Alterações por Arquivo

### 1. scripts/1_coleta_grafo_ondina.py
- Adicionada função `collect_points_of_interest` para coletar POIs do OpenStreetMap
- Incluídos novos tipos de POIs:
  - Pontos turísticos (tourism)
  - Serviços (restaurantes, cafés, bancos, caixas eletrônicos, escolas, universidades)
  - Comércio (shops)
  - Áreas de lazer (leisure)
- Adicionada coleta de pontos de ônibus como locais de coleta de passageiros
- Implementada atribuição de valores de bônus aos POIs
- Adicionados atributos aos nós do grafo:
  - `is_poi`: Indica se é um ponto de interesse
  - `poi_type`: Tipo do POI
  - `poi_name`: Nome do local
  - `bonus_value`: Valor do bônus (padrão: 10)
  - `is_bus_stop`: Indica se é ponto de ônibus
  - `passenger_pickup`: Indica possibilidade de coleta de passageiros

### 2. scripts/2_gera_instancia.py
- Nova estrutura de dados para a instância incluindo:
  - Lista de POIs com bônus
  - Lista de pontos de coleta de passageiros
  - Parâmetros do problema
- Adicionados novos campos nas arestas:
  - Tempo estimado de viagem
  - Nome da rua
- Implementados parâmetros do problema:
  - Capacidade do veículo (4 passageiros)
  - Tempo máximo de rota (8 horas)
  - Multiplicador de bônus (1.5x)
  - Recompensa por passageiro (50 pontos)
- Novo formato de arquivo de saída: `ondina_tsp_bc_pp.json`

### 3. scripts/3_visualiza_instancia.py
- Implementada visualização diferenciada para:
  - POIs (vermelho, tamanho 100)
  - Pontos de passageiros (azul, tamanho 80)
  - Interseções normais (preto, tamanho 20)
- Adicionadas legendas para:
  - Nome e valor do bônus dos POIs
  - Capacidade dos pontos de passageiros
- Incluída legenda geral do grafo
- Novo título refletindo o problema TSP-BC-PP

### 4. scripts/4_analisa_instancia.py
- Novas métricas de análise:
  - Estatísticas de POIs (quantidade, tipos, bônus total)
  - Estatísticas de pontos de passageiros (quantidade, capacidade)
  - Análise de tempos e distâncias
  - Parâmetros do problema
- Implementada análise de viabilidade:
  - Estimativa de distância total
  - Estimativa de tempo total
  - Alerta de viabilidade temporal
  - Cálculo de recompensa potencial máxima

## Como Testar as Mudanças

1. Execute os scripts na ordem:
```bash
python3 scripts/1_coleta_grafo_ondina.py
python3 scripts/2_gera_instancia.py
python3 scripts/3_visualiza_instancia.py
python3 scripts/4_analisa_instancia.py
```

2. Verifique os arquivos gerados:
- `scripts/grafo_ondina.gpickle`: Grafo com POIs e pontos de passageiros
- `instancias/ondina_tsp_bc_pp.json`: Instância formatada do problema

3. Analise a visualização gerada:
- Pontos vermelhos: POIs
- Pontos azuis: Locais de coleta de passageiros
- Legendas com informações de bônus e capacidades

4. Revise o relatório de análise para:
- Confirmar a presença de POIs e pontos de passageiros
- Verificar a viabilidade da solução
- Avaliar as recompensas potenciais

## Próximos Passos
1. Implementar algoritmos de solução para o TSP-BC-PP
2. Adicionar restrições de janelas de tempo para POIs
3. Implementar diferentes estratégias de coleta de passageiros
4. Desenvolver visualização da solução encontrada
5. Criar métricas de avaliação da qualidade da solução 