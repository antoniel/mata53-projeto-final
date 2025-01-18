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
        "nodes": [],
        "edges": [],
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
            "lat": data['y'],
            "lon": data['x']
        })
    
    # Adicionar arestas
    for u, v, data in G.edges(data=True):
        if 'length' in data:
            peso = data['length']
        else:
            peso = ((G.nodes[u]['y'] - G.nodes[v]['y'])**2 + 
                   (G.nodes[u]['x'] - G.nodes[v]['x'])**2)**0.5 * 111000
        
        edge = {
            "source": mapeamento_nos[u],
            "target": mapeamento_nos[v],
            "weight": float(peso),
            "name": data.get('name', '')
        }
        instancia["edges"].append(edge)
    
    # Calcular cobertura de vértices
    vertex_cover = nx.approximation.min_weighted_vertex_cover(G)
    instancia["vertex_cover"] = [mapeamento_nos[node] for node in vertex_cover]
    
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
    grafo_path = "grafo_ondina.gpickle"
    output_dir = "../instancias"
    
    cria_instancia_do_grafo(grafo_path, output_dir) 