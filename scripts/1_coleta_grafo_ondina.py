import osmnx as ox
import networkx as nx
import pickle

# Nome do bairro ou área de interesse
bairro = "Ondina, Salvador, Brazil"

# Baixar o grafo do bairro da Ondina
print("Baixando dados do OpenStreetMap...")
grafo = ox.graph_from_place(bairro, network_type='drive')

# Criar uma figura maior para melhor visualização
# plt.figure(figsize=(20, 20))

# Plotar o grafo base com cores personalizadas
# ox.plot_graph(grafo, 
#               node_size=20,
#               node_color='black',
#               edge_color='black',
#               edge_linewidth=1,
#               bgcolor='white',
#               show=False)

# Adicionar os nomes das ruas nas arestas
# for u, v, data in grafo.edges(data=True):
#     if 'name' in data:
#         # Pegar o ponto médio da aresta para posicionar o texto
#         mid_point = [
#             (grafo.nodes[u]['y'] + grafo.nodes[v]['y']) / 2,
#             (grafo.nodes[u]['x'] + grafo.nodes[v]['x']) / 2
#         ]
#         # Simplificar o nome da rua
#         nome = data['name']
#         if isinstance(nome, list):
#             nome = nome[0]  # Pega o primeiro nome se for uma lista
#         if nome.lower().startswith(('rua ', 'avenida ')):
#             nome = nome.split(' ', 1)[1]  # Remove 'Rua' ou 'Avenida' do início
#         plt.text(mid_point[1], mid_point[0], nome, 
#                 fontsize=6,  # Fonte menor
#                 ha='center',
#                 va='center',
#                 bbox=dict(facecolor='white', 
#                          edgecolor='none',
#                          alpha=0.8,
#                          pad=0.5),
#                 rotation=45,
#                 zorder=3)

# plt.tight_layout()
# plt.show()

# Exportar o grafo para análise posterior
print("Salvando o grafo...")
with open("grafo_ondina.gpickle", 'wb') as f:
    pickle.dump(grafo, f)
print("Grafo salvo com sucesso em: grafo_ondina.gpickle")