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
            weight=edge['weight'],
            # name=edge['name']
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
    
    # Adicionar os nomes das ruas
    print("Adicionando nomes das ruas...")
    edge_labels = {}
    # for edge in data['edges']:
    #     if edge['name']:  # Se tiver nome
    #         # Pegar o ponto médio da aresta para o texto
    #         source_pos = pos[edge['source']]
    #         target_pos = pos[edge['target']]
    #         mid_x = (source_pos[0] + target_pos[0]) / 2
    #         mid_y = (source_pos[1] + target_pos[1]) / 2
            
    #         # Simplificar o nome da rua
    #         nome = edge['name']
    #         if isinstance(nome, list):
    #             nome = nome[0]
    #         if nome.lower().startswith(('rua ', 'avenida ')):
    #             nome = nome.split(' ', 1)[1]
            
    #         # Adicionar o texto
    #         plt.text(
    #             mid_x, mid_y, 
    #             nome,
    #             fontsize=6,
    #             ha='center',
    #             va='center',
    #             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.5),
    #             rotation=45
    #         )
    
    plt.title("Grafo de Ondina")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Caminho para o arquivo JSON
    json_path = "../instancias/ondina.json"
    
    visualiza_grafo(json_path) 