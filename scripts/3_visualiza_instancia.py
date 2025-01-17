import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def format_poi_name(name, poi_type):
    """Formata o nome do POI para exibição"""
    if name == 'Unknown' or name == 'nan':
        if poi_type:
            return poi_type.title().replace('_', ' ')
        return 'Ponto de Interesse'
    return name

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
    node_colors = []
    node_sizes = []
    
    # Criar conjuntos de nós especiais
    poi_nodes = {poi['node_id'] for poi in data['points_of_interest']}
    passenger_nodes = {pp['node_id'] for pp in data['passenger_points']}
    
    # Configurar estilo do plot
    plt.style.use('seaborn')
    plt.figure(figsize=(20, 20), facecolor='white')
    
    # Adicionar nós
    for node in data['nodes']:
        G.add_node(node['id'])
        pos[node['id']] = (node['lon'], node['lat'])
        
        # Definir cores e tamanhos dos nós
        if node['id'] in poi_nodes:
            node_colors.append('#FF6B6B')  # Vermelho suave
            node_sizes.append(150)
        elif node['id'] in passenger_nodes:
            node_colors.append('#4ECDC4')  # Azul turquesa
            node_sizes.append(100)
        else:
            node_colors.append('#2C3E50')  # Azul escuro
            node_sizes.append(30)
    
    # Adicionar arestas
    print("Adicionando arestas...")
    for edge in data['edges']:
        G.add_edge(
            edge['source'], 
            edge['target'], 
            weight=edge['weight'],
            time=edge['time']
        )
    
    # Desenhar o grafo base
    print("Desenhando o grafo...")
    nx.draw(
        G, 
        pos=pos,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color='#95A5A6',  # Cinza suave
        width=1,
        alpha=0.7,
        with_labels=False
    )
    
    # Adicionar legendas para POIs
    print("Adicionando legendas...")
    for poi in data['points_of_interest']:
        node_pos = pos[poi['node_id']]
        poi_name = format_poi_name(poi['name'], poi['type'])
        plt.text(
            node_pos[0], node_pos[1] + 0.0001,
            f"{poi_name}\n💎 {poi['bonus_value']}",
            fontsize=8,
            ha='center',
            va='bottom',
            bbox=dict(
                facecolor='white',
                alpha=0.9,
                edgecolor='#FF6B6B',
                boxstyle='round,pad=0.5'
            )
        )
    
    # Adicionar legendas para pontos de passageiros
    for pp in data['passenger_points']:
        node_pos = pos[pp['node_id']]
        plt.text(
            node_pos[0], node_pos[1] - 0.0001,
            f"🚌 Ponto de Ônibus\n👥 {pp['capacity']}",
            fontsize=8,
            ha='center',
            va='top',
            bbox=dict(
                facecolor='white',
                alpha=0.9,
                edgecolor='#4ECDC4',
                boxstyle='round,pad=0.5'
            )
        )
    
    # Adicionar legenda
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', 
                  markerfacecolor='#2C3E50', markersize=8,
                  label='Interseções'),
        plt.Line2D([0], [0], marker='o', color='w',
                  markerfacecolor='#FF6B6B', markersize=12,
                  label='Pontos de Interesse'),
        plt.Line2D([0], [0], marker='o', color='w',
                  markerfacecolor='#4ECDC4', markersize=10,
                  label='Pontos de Ônibus')
    ]
    
    plt.legend(handles=legend_elements,
              fontsize=12,
              loc='upper left',
              bbox_to_anchor=(1.05, 1),
              title='Legenda',
              title_fontsize=14,
              frameon=True,
              facecolor='white',
              edgecolor='#95A5A6')
    
    # Configurar título e layout
    plt.title("Mapa de Ondina - TSP com Coleta de Bônus e Passageiros",
             pad=20,
             fontsize=16,
             fontweight='bold')
    
    plt.tight_layout()
    
    # Adicionar informações do problema
    info_text = (
        f"Total de POIs: {len(data['points_of_interest'])}\n"
        f"Total de Pontos de Ônibus: {len(data['passenger_points'])}\n"
        f"Bônus Total Disponível: {sum(poi['bonus_value'] for poi in data['points_of_interest'])}\n"
        f"Capacidade Total de Passageiros: {sum(pp['capacity'] for pp in data['passenger_points'])}"
    )
    plt.figtext(0.02, 0.02, info_text,
                fontsize=10,
                bbox=dict(facecolor='white',
                         alpha=0.9,
                         edgecolor='#95A5A6',
                         boxstyle='round,pad=0.5'))
    
    # Salvar e mostrar
    plt.savefig('../instancias/mapa_ondina.png', 
                dpi=300,
                bbox_inches='tight',
                facecolor='white')
    plt.show()

if __name__ == "__main__":
    # Caminho para o arquivo JSON
    json_path = "../instancias/ondina_tsp_bc_pp.json"
    visualiza_grafo(json_path) 