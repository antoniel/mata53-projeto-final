import json
import networkx as nx
import matplotlib.pyplot as plt

def visualiza_grafo(json_path):
    # Carregar o JSON
    print("Carregando dados do arquivo JSON...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Criar um grafo direcionado
    G = nx.Graph()
    
    # Adicionar nós com suas posições
    print("Criando grafo...")
    pos = {}
    for node in data['nodes']:
        G.add_node(node['id'])
        # Usar longitude como x e latitude como y
        pos[node['id']] = (node['lon'], node['lat'])
    
    # Adicionar arestas
    for edge in data['edges']:
        G.add_edge(
            edge['source'], 
            edge['target'], 
            weight=edge['weight']
        )
    
    # Configurar o plot
    plt.figure(figsize=(20, 20))
    
    # Desenhar o grafo
    print("Desenhando o grafo...")
    nx.draw(
        G, 
        pos=pos,
        node_color='black',
        node_size=20,
        edge_color='gray',
        width=1,
        with_labels=False
    )
    
    # Highlight vertex cover nodes
    vertex_cover = data.get("vertex_cover", [])
    nx.draw_networkx_nodes(
        G, 
        pos, 
        nodelist=vertex_cover, 
        node_color='red', 
        node_size=50,
        label='Vertex Cover Nodes'
    )
    
    # Add labels for edges with names
    for edge in data['edges']:
        if edge['name']:
            mid_x = (pos[edge['source']][0] + pos[edge['target']][0]) / 2
            mid_y = (pos[edge['source']][1] + pos[edge['target']][1]) / 2
            plt.text(mid_x, mid_y, edge['name'], fontsize=6, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.5))
    
    plt.title("Grafo de Ondina com Cobertura de Vértices")
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Caminho para o arquivo JSON
    json_path = "../instancias/ondina.json"
    
    visualiza_grafo(json_path) 