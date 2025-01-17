import json
import networkx as nx
from collections import Counter
import numpy as np

def analisa_instancia(json_path):
    # Carregar o JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Estatísticas básicas
    num_nos = len(data['nodes'])
    num_arestas = len(data['edges'])
    num_pois = len(data['points_of_interest'])
    num_passenger_points = len(data['passenger_points'])
    
    # Criar grafo para análises
    G = nx.Graph()
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'], 
                  weight=edge['weight'],
                  time=edge['time'])
    
    # Análise de conectividade
    num_componentes = nx.number_connected_components(G)
    
    # Análise de POIs
    total_bonus = sum(poi['bonus_value'] for poi in data['points_of_interest'])
    tipos_poi = Counter(poi['type'] for poi in data['points_of_interest'])
    
    # Análise de pontos de passageiros
    total_capacidade = sum(pp['capacity'] for pp in data['passenger_points'])
    
    # Análise de tempos e distâncias
    tempos = [edge['time'] for edge in data['edges']]
    distancias = [edge['weight'] for edge in data['edges']]
    
    # Análise de parâmetros do problema
    params = data['parameters']
    
    # Gerar relatório
    print("\n=== ANÁLISE DA INSTÂNCIA TSP-BC-PP DE ONDINA ===\n")
    
    print("ESTATÍSTICAS BÁSICAS:")
    print(f"- Número de nós (interseções): {num_nos}")
    print(f"- Número de arestas (trechos de ruas): {num_arestas}")
    print(f"- Número de componentes conectados: {num_componentes}")
    
    print("\nPONTOS DE INTERESSE (POIs):")
    print(f"- Número total de POIs: {num_pois}")
    print(f"- Valor total de bônus disponível: {total_bonus}")
    print(f"- Média de bônus por POI: {total_bonus/num_pois if num_pois > 0 else 0:.2f}")
    print("\nTipos de POIs:")
    for tipo, count in tipos_poi.most_common():
        print(f"  - {tipo}: {count}")
    
    print("\nPONTOS DE PASSAGEIROS:")
    print(f"- Número de pontos de coleta: {num_passenger_points}")
    print(f"- Capacidade total de passageiros: {total_capacidade}")
    print(f"- Média de capacidade por ponto: {total_capacidade/num_passenger_points if num_passenger_points > 0 else 0:.2f}")
    
    print("\nANÁLISE DE TEMPOS E DISTÂNCIAS:")
    print(f"- Tempo médio entre nós: {np.mean(tempos):.2f} minutos")
    print(f"- Tempo máximo entre nós: {max(tempos):.2f} minutos")
    print(f"- Distância média entre nós: {np.mean(distancias):.2f} metros")
    print(f"- Distância máxima entre nós: {max(distancias):.2f} metros")
    
    print("\nPARÂMETROS DO PROBLEMA:")
    print(f"- Capacidade do veículo: {params['vehicle_capacity']} passageiros")
    print(f"- Tempo máximo de rota: {params['max_time']} minutos")
    print(f"- Multiplicador de bônus: {params['bonus_multiplier']}")
    print(f"- Recompensa por passageiro: {params['passenger_reward']}")
    
    print("\nMÉTRICAS DE REDE:")
    print(f"- Densidade do grafo: {nx.density(G):.4f}")
    print(f"- Diâmetro do grafo: {nx.diameter(G)}")
    print(f"- Grau médio dos nós: {sum(dict(G.degree()).values())/num_nos:.2f}")
    
    # Análise de viabilidade
    print("\nANÁLISE DE VIABILIDADE:")
    max_dist = max(distancias)
    total_dist_estimate = max_dist * (num_pois + num_passenger_points)
    total_time_estimate = total_dist_estimate / 30.0  # assumindo 30 m/min
    
    print(f"- Estimativa de distância total para visitar todos os pontos: {total_dist_estimate/1000:.2f} km")
    print(f"- Estimativa de tempo total: {total_time_estimate:.2f} minutos")
    if total_time_estimate > params['max_time']:
        print("! ALERTA: Pode não ser possível visitar todos os pontos no tempo máximo permitido")
    
    max_passengers = min(total_capacidade, params['vehicle_capacity'])
    potential_reward = (total_bonus * params['bonus_multiplier'] + 
                       max_passengers * params['passenger_reward'])
    print(f"- Recompensa potencial máxima: {potential_reward:.2f}")

if __name__ == "__main__":
    # Caminho para o arquivo JSON
    json_path = "../instancias/ondina_tsp_bc_pp.json"
    analisa_instancia(json_path) 