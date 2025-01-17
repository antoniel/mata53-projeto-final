import networkx as nx
import json
import os
import pickle

def cria_instancia_do_grafo(grafo_path, output_dir):
    # Carregar o grafo
    with open(grafo_path, 'rb') as f:
        G = pickle.load(f)
    
    # Criar dicionário de mapeamento de nós
    mapeamento_nos = {node: idx for idx, node in enumerate(G.nodes())}
    
    # Criar a estrutura da instância
    instancia = {
        "nodes": [],  # Lista de nós com suas coordenadas
        "edges": [],  # Lista de arestas com seus pesos
        "points_of_interest": [],  # Lista de POIs com bônus
        "passenger_points": [],  # Pontos de coleta de passageiros
        "metadata": {
            "name": "Grafo de Ondina - TSP com Coleta de Bônus e Passageiros",
            "description": "Instância para o problema do caixeiro viajante com coleta de bônus e passageiros no bairro de Ondina",
            "source": "OpenStreetMap"
        }
    }
    
    # Adicionar nós
    for node_id, data in G.nodes(data=True):
        node_info = {
            "id": mapeamento_nos[node_id],
            "lat": data['y'],  # Latitude
            "lon": data['x']   # Longitude
        }
        
        # Adicionar informações de POI se existirem
        if data.get('is_poi', False):
            poi_info = {
                "node_id": mapeamento_nos[node_id],
                "type": data.get('poi_type', 'unknown'),
                "name": data.get('poi_name', 'Unknown'),
                "bonus_value": data.get('bonus_value', 10)
            }
            instancia["points_of_interest"].append(poi_info)
        
        # Adicionar informações de ponto de passageiros se existirem
        if data.get('is_bus_stop', False):
            passenger_info = {
                "node_id": mapeamento_nos[node_id],
                "type": "bus_stop",
                "capacity": 4  # Capacidade padrão de passageiros
            }
            instancia["passenger_points"].append(passenger_info)
        
        instancia["nodes"].append(node_info)
    
    # Adicionar arestas
    for u, v, data in G.edges(data=True):
        # Calcular o peso da aresta (comprimento em metros)
        if 'length' in data:
            peso = data['length']
        else:
            # Se não tiver comprimento, usar distância euclidiana
            peso = ((G.nodes[u]['y'] - G.nodes[v]['y'])**2 + 
                   (G.nodes[u]['x'] - G.nodes[v]['x'])**2)**0.5 * 111000
        
        edge = {
            "source": mapeamento_nos[u],
            "target": mapeamento_nos[v],
            "weight": float(peso),  # Peso em metros
            "name": data.get('name', ''),  # Nome da rua se disponível
            "time": float(peso) / 30.0  # Tempo estimado em minutos (assumindo 30 m/min)
        }
        instancia["edges"].append(edge)
    
    # Adicionar parâmetros do problema
    instancia["parameters"] = {
        "vehicle_capacity": 4,  # Capacidade máxima do veículo
        "max_time": 480,  # Tempo máximo da rota (8 horas em minutos)
        "bonus_multiplier": 1.5,  # Multiplicador de bônus por visita
        "passenger_reward": 50  # Recompensa por passageiro entregue
    }
    
    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Salvar a instância em formato JSON
    output_path = os.path.join(output_dir, "ondina_tsp_bc_pp.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(instancia, f, indent=2, ensure_ascii=False)
    
    print(f"Instância gerada com sucesso!")
    print(f"Número de nós: {len(instancia['nodes'])}")
    print(f"Número de arestas: {len(instancia['edges'])}")
    print(f"Número de POIs: {len(instancia['points_of_interest'])}")
    print(f"Número de pontos de passageiros: {len(instancia['passenger_points'])}")
    print(f"Arquivo salvo em: {output_path}")

if __name__ == "__main__":
    grafo_path = "grafo_ondina.gpickle"
    output_dir = "../instancias"
    cria_instancia_do_grafo(grafo_path, output_dir) 