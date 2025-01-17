import json
import networkx as nx
from collections import Counter

def analisa_instancia(json_path):
    # Carregar o JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Estatísticas básicas
    num_nos = len(data['nodes'])
    num_arestas = len(data['edges'])
    
    # Criar grafo para análises
    G = nx.Graph()
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    # Análise de conectividade
    num_componentes = nx.number_connected_components(G)
    
    # Análise de ruas
    ruas = []
    comprimento_total = 0
    for edge in data['edges']:
        if edge['name']:
            if isinstance(edge['name'], list):
                ruas.extend(edge['name'])
            else:
                ruas.append(edge['name'])
        comprimento_total += edge['weight']
    
    # Contagem de ruas
    contagem_ruas = Counter(ruas)
    ruas_principais = sorted(contagem_ruas.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Limites geográficos
    lat_min = min(node['lat'] for node in data['nodes'])
    lat_max = max(node['lat'] for node in data['nodes'])
    lon_min = min(node['lon'] for node in data['nodes'])
    lon_max = max(node['lon'] for node in data['nodes'])
    
    vertex_cover = data.get("vertex_cover", [])
    
    # Gerar relatório
    print("\n=== ANÁLISE DA INSTÂNCIA DO GRAFO DE ONDINA ===\n")
    
    print("ESTATÍSTICAS BÁSICAS:")
    print(f"- Número de nós (interseções): {num_nos}")
    print(f"- Número de arestas (trechos de ruas): {num_arestas}")
    print(f"- Número de componentes conectados: {num_componentes}")
    print(f"- Comprimento total das ruas: {comprimento_total/1000:.2f} km")
    
    print("\nLIMITES GEOGRÁFICOS:")
    print(f"- Latitude: {lat_min:.6f} a {lat_max:.6f}")
    print(f"- Longitude: {lon_min:.6f} a {lon_max:.6f}")
    
    print("\nRUAS PRINCIPAIS (top 5 por número de trechos):")
    for rua, count in ruas_principais:
        print(f"- {rua}: {count} trechos")
    
    print("\nMÉTRICAS DE REDE:")
    print(f"- Densidade do grafo: {nx.density(G):.4f}")
    print(f"- Diâmetro do grafo: {nx.diameter(G)}")
    print(f"- Grau médio dos nós: {sum(dict(G.degree()).values())/num_nos:.2f}")
    
    print("\nCOBERTURA DE VÉRTICES:")
    print(f"- Número de nós na cobertura de vértices: {len(vertex_cover)}")
    print(f"- Nós na cobertura de vértices: {vertex_cover}")

if __name__ == "__main__":
    # Caminho para o arquivo JSON
    json_path = "../instancias/ondina.json"
    
    analisa_instancia(json_path) 