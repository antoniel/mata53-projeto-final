import json
import networkx as nx
import matplotlib.pyplot as plt
import os
from pathlib import Path

def visualiza_cobertura(json_path, resultados_dir, figuras_dir):
    # Carregar o grafo original
    print("Carregando dados do arquivo JSON...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Carregar resultados da cobertura
    print("Carregando resultados da cobertura...")
    with open(f"{resultados_dir}/cobertura_completa.json", 'r') as f:
        cobertura_completa = json.load(f)
    with open(f"{resultados_dir}/cobertura_maxima.json", 'r') as f:
        cobertura_maxima = json.load(f)
    
    # Criar grafo
    G = nx.Graph()
    pos = {}
    
    # Adicionar nós com suas posições
    print("Criando grafo...")
    for node in data['nodes']:
        G.add_node(node['id'])
        pos[node['id']] = (node['lon'], node['lat'])
    
    # Adicionar arestas
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    # Criar duas visualizações lado a lado
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Cobertura Completa
    print("Desenhando cobertura completa...")
    nx.draw(G, pos=pos, node_color='lightgray', node_size=20, 
            edge_color='gray', width=1, with_labels=False, ax=ax1)
    
    # Destacar câmeras e vértices cobertos
    cameras_completa = cobertura_completa.get('vertices_selecionados', [])
    vertices_cobertos_completa = set()
    for camera in cameras_completa:
        vertices_cobertos_completa.add(camera)  # A própria câmera
        vertices_cobertos_completa.update(G.neighbors(camera))  # Vizinhos da câmera
    
    nx.draw_networkx_nodes(G, pos, nodelist=cameras_completa, 
                          node_color='red', node_size=100, 
                          label='Câmeras', ax=ax1)
    
    ax1.set_title(f"Cobertura Completa\n{len(cameras_completa)} câmeras cobrindo {len(vertices_cobertos_completa)} vértices")
    ax1.legend()
    
    # Cobertura Máxima
    print("Desenhando cobertura máxima...")
    nx.draw(G, pos=pos, node_color='lightgray', node_size=20, 
            edge_color='gray', width=1, with_labels=False, ax=ax2)
    
    # Destacar câmeras e vértices cobertos
    cameras_maxima = cobertura_maxima.get('vertices_selecionados', [])
    vertices_cobertos_maxima = set()
    for camera in cameras_maxima:
        vertices_cobertos_maxima.add(camera)  # A própria câmera
        vertices_cobertos_maxima.update(G.neighbors(camera))  # Vizinhos da câmera
    vertices_cobertos_maxima = list(vertices_cobertos_maxima)
    
    nx.draw_networkx_nodes(G, pos, nodelist=cameras_maxima, 
                          node_color='red', node_size=100, 
                          label='Câmeras', ax=ax2)
    nx.draw_networkx_nodes(G, pos, nodelist=vertices_cobertos_maxima, 
                          node_color='green', node_size=50, 
                          label='Vértices Cobertos', ax=ax2)
    
    ax2.set_title(f"Cobertura Máxima\n{len(cameras_maxima)} câmeras cobrindo {len(vertices_cobertos_maxima)} vértices")
    ax2.legend()
    
    plt.tight_layout()
    
    # Criar diretório Figuras se não existir
    os.makedirs(figuras_dir, exist_ok=True)
    
    # Salvar em ambos os diretórios
    plt.savefig(f"{resultados_dir}/visualizacao_cobertura.png", dpi=300, bbox_inches='tight')
    plt.savefig(f"{figuras_dir}/visualizacao_cobertura.png", dpi=300, bbox_inches='tight')
    print(f"Visualização salva em:")
    print(f"- {resultados_dir}/visualizacao_cobertura.png")
    print(f"- {figuras_dir}/visualizacao_cobertura.png")
    plt.close()

if __name__ == "__main__":
    # Determinar caminhos relativos ao script
    script_dir = Path(__file__).parent.parent  # Diretório raiz do projeto
    json_path = script_dir / "instancias" / "ondina.json"
    resultados_dir = script_dir / "resultados"
    figuras_dir = script_dir / "Figuras"
    
    visualiza_cobertura(json_path, resultados_dir, figuras_dir) 