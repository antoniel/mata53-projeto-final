import networkx as nx
import json
import os
import pickle

def cria_instancia_do_grafo(grafo_path, output_dir):
    # Carregar o grafo
    with open(grafo_path, 'rb') as f:
        G = pickle.load(f)
    
    # Criar dicionário de mapeamento de nós
    # Mapear os IDs originais do OSM para números sequenciais
    mapeamento_nos = {node: idx for idx, node in enumerate(G.nodes())}
    
    # Criar a estrutura da instância
    instancia = {
        "nodes": [],  # Lista de nós com suas coordenadas
        "edges": [],  # Lista de arestas com seus pesos
        "metadata": {
            "name": "Grafo de Ondina",
            "description": "Grafo das ruas do bairro de Ondina, Salvador",
            "source": "OpenStreetMap"
        }
    }
    
    # Adicionar nós
    for node_id, data in G.nodes(data=True):
        instancia["nodes"].append({
            "id": mapeamento_nos[node_id],
            "lat": data['y'],  # Latitude
            "lon": data['x']   # Longitude
        })
    
    # Adicionar arestas
    for u, v, data in G.edges(data=True):
        # Calcular o peso da aresta (comprimento em metros)
        if 'length' in data:
            peso = data['length']
        else:
            # Se não tiver comprimento, usar distância euclidiana
            peso = ((G.nodes[u]['y'] - G.nodes[v]['y'])**2 + 
                   (G.nodes[u]['x'] - G.nodes[v]['x'])**2)**0.5 * 111000  # Aproximação em metros
        
        # Adicionar a aresta com seu peso
        edge = {
            "source": mapeamento_nos[u],
            "target": mapeamento_nos[v],
            "weight": float(peso),  # Peso em metros
            "name": data.get('name', '')  # Nome da rua se disponível
        }
        instancia["edges"].append(edge)
    
    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Salvar a instância em formato JSON
    output_path = os.path.join(output_dir, "ondina.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(instancia, f, indent=2, ensure_ascii=False)
    
    print(f"Instância gerada com sucesso!")
    print(f"Número de nós: {len(instancia['nodes'])}")
    print(f"Número de arestas: {len(instancia['edges'])}")
    print(f"Arquivo salvo em: {output_path}")

if __name__ == "__main__":
    # Caminho do grafo pickle gerado pelo script anterior
    grafo_path = "grafo_ondina.gpickle"
    
    # Diretório onde a instância será salva
    output_dir = "../instancias"
    
    cria_instancia_do_grafo(grafo_path, output_dir) 