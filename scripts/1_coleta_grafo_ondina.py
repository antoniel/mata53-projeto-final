import osmnx as ox
import networkx as nx
import pickle
import pandas as pd
from shapely.geometry import Point

# Nome do bairro ou área de interesse
bairro = "Ondina, Salvador, Brazil"

def collect_points_of_interest(place):
    """Coleta pontos de interesse do OpenStreetMap"""
    tags = {
        'tourism': True,  # Pontos turísticos
        'amenity': ['restaurant', 'cafe', 'bank', 'atm', 'school', 'university'],  # Serviços
        'shop': True,  # Comércio
        'leisure': True  # Lazer
    }
    
    # Usar geometries_from_place em vez de features_from_place
    pois = ox.geometries_from_place(place, tags=tags)
    return pois

# Configurar o grafo para usar projeção UTM
print("Baixando dados do OpenStreetMap...")
grafo = ox.graph_from_place(bairro, network_type='drive', simplify=True)
grafo = ox.project_graph(grafo)

# Coletar pontos de interesse
print("Coletando pontos de interesse...")
pois = collect_points_of_interest(bairro)

# Projetar os POIs para o mesmo sistema de coordenadas do grafo
pois = ox.project_gdf(pois)

# Adicionar informações dos POIs ao grafo
print("Processando pontos de interesse...")
for idx, poi in pois.iterrows():
    try:
        # Usar o centro do polígono se for uma área
        if poi.geometry.geom_type == 'Polygon':
            point = poi.geometry.centroid
        else:
            point = poi.geometry
        
        # Encontrar o nó mais próximo no grafo
        nearest_node = ox.distance.nearest_nodes(grafo, point.x, point.y)
        
        # Adicionar atributos ao nó
        grafo.nodes[nearest_node]['is_poi'] = True
        grafo.nodes[nearest_node]['poi_type'] = poi.get('amenity') or poi.get('tourism') or poi.get('shop') or poi.get('leisure')
        grafo.nodes[nearest_node]['poi_name'] = poi.get('name', 'Unknown')
        grafo.nodes[nearest_node]['bonus_value'] = 10  # Valor padrão de bônus para POIs
    except Exception as e:
        print(f"Erro ao processar POI: {e}")
        continue

# Adicionar pontos de ônibus como possíveis locais de coleta de passageiros
print("Coletando pontos de ônibus...")
try:
    bus_stops = ox.geometries_from_place(bairro, tags={'highway': 'bus_stop'})
    bus_stops = ox.project_gdf(bus_stops)
    
    for idx, stop in bus_stops.iterrows():
        try:
            point = stop.geometry.centroid if stop.geometry.geom_type == 'Polygon' else stop.geometry
            nearest_node = ox.distance.nearest_nodes(grafo, point.x, point.y)
            grafo.nodes[nearest_node]['is_bus_stop'] = True
            grafo.nodes[nearest_node]['passenger_pickup'] = True
        except Exception as e:
            print(f"Erro ao processar ponto de ônibus: {e}")
            continue
except Exception as e:
    print(f"Erro ao coletar pontos de ônibus: {e}")

# Exportar o grafo para análise posterior
print("Salvando o grafo...")
with open("grafo_ondina.gpickle", 'wb') as f:
    pickle.dump(grafo, f)
print("Grafo salvo com sucesso em: grafo_ondina.gpickle")