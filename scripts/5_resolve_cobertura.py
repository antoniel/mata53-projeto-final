#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
from typing import List, Set, Tuple
import json
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_graph_from_json(json_path: str) -> nx.Graph:
    """
    Carrega o grafo a partir do arquivo JSON.
    
    Args:
        json_path (str): Caminho para o arquivo JSON
        
    Returns:
        nx.Graph: Grafo do NetworkX
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Cria um grafo não direcionado
    G = nx.Graph()
    
    # Adiciona os nós com seus atributos
    for node in data['nodes']:
        G.add_node(
            node['id'],
            lat=node['lat'],
            lon=node['lon']
        )
    
    # Adiciona as arestas com seus atributos
    for edge in data['edges']:
        G.add_edge(
            edge['source'],
            edge['target'],
            weight=edge['weight'],
            name=edge.get('name', '')  # Alguns podem não ter nome
        )
    
    return G

class CoberturaVertices:
    def __init__(self, grafo: nx.Graph):
        """
        Inicializa o solver de cobertura de vértices.
        
        Args:
            grafo (nx.Graph): Grafo do NetworkX representando a malha viária
        """
        self.grafo = grafo
        self.I = list(grafo.nodes())  # conjunto de vértices de demanda
        self.J = list(grafo.nodes())  # conjunto de vértices de instalação
        self.cameras = {}  # dicionário para armazenar as câmeras instaladas
        
        # Inicialização da matriz de adjacência
        self.matriz_adjacencia = nx.adjacency_matrix(grafo).toarray()  # matriz de adjacência
        
    def resolve_cobertura_completa(self) -> Set[int]:
        """
        Implementa o algoritmo guloso para cobertura completa de vértices.
        Uma câmera instalada em um vértice cobre todos os vértices adjacentes
        e o próprio vértice.
        
        Returns:
            Set[int]: Conjunto de vértices selecionados para instalação de câmeras
        """
        vertices_nao_cobertos = set(self.I)
        cobertura = set()
        
        while vertices_nao_cobertos:
            # Encontra o vértice que cobre mais vértices ainda não cobertos
            melhor_vertice = None
            max_cobertura = 0
            
            for v in self.J:
                if v not in cobertura:
                    # Calcula quantos vértices não cobertos este vértice pode cobrir
                    vizinhos = set(self.grafo.neighbors(v))
                    cobertura_atual = len((vizinhos | {v}) & vertices_nao_cobertos)
                    
                    if cobertura_atual > max_cobertura:
                        max_cobertura = cobertura_atual
                        melhor_vertice = v
            
            if melhor_vertice is None:
                break
                
            # Adiciona o melhor vértice à cobertura
            cobertura.add(melhor_vertice)
            
            # Atualiza os vértices não cobertos
            vertices_nao_cobertos -= set(self.grafo.neighbors(melhor_vertice))
            vertices_nao_cobertos.discard(melhor_vertice)
            
        return cobertura

    def resolve_cobertura_maxima(self, max_cameras: int = 40) -> Tuple[List[int], Set[int]]:
        """
        Resolve o problema de cobertura máxima, onde queremos cobrir o máximo
        de vértices possível usando no máximo max_cameras câmeras.
        
        Args:
            max_cameras: Número máximo de câmeras que podem ser usadas.
            
        Returns:
            Tupla com (lista de vértices selecionados, conjunto de vértices cobertos)
        """
        cobertura = set()
        vertices_cobertos = set()
        
        for _ in range(max_cameras):
            melhor_vertice = None
            max_novos_cobertos = 0
            
            for v in self.J:
                if v not in cobertura:
                    # Calcula quantos novos vértices seriam cobertos
                    vizinhos = set(self.grafo.neighbors(v))
                    novos_cobertos = len((vizinhos | {v}) - vertices_cobertos)
                    
                    if novos_cobertos > max_novos_cobertos:
                        max_novos_cobertos = novos_cobertos
                        melhor_vertice = v
            
            if melhor_vertice is None or max_novos_cobertos == 0:
                break
                
            # Adiciona o melhor vértice à cobertura
            cobertura.add(melhor_vertice)
            
            # Atualiza os vértices cobertos
            vertices_cobertos.update(self.grafo.neighbors(melhor_vertice))
            vertices_cobertos.add(melhor_vertice)
            
        return list(cobertura), vertices_cobertos

    def salvar_resultado(self, cobertura: Set[int], arquivo_saida: str, vertices_cobertos: Set[int] = None):
        """
        Salva o resultado da cobertura em um arquivo JSON.
        
        Args:
            cobertura (Set[int]): Conjunto de vértices selecionados
            arquivo_saida (str): Caminho do arquivo de saída
            vertices_cobertos (Set[int], optional): Conjunto de vértices cobertos
        """
        if vertices_cobertos is None:
            vertices_cobertos = set().union(*[set(self.grafo.neighbors(v)) | {v} for v in cobertura])
            
        resultado = {
            "vertices_selecionados": list(cobertura),
            "vertices_cobertos": list(vertices_cobertos),
            "num_cameras": len(cobertura),
            "total_cobertura": len(vertices_cobertos),
            "total_vertices": len(self.grafo)
        }
        
        os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)
        with open(arquivo_saida, 'w') as f:
            json.dump(resultado, f, indent=2)
            
def main():
    # Carrega o grafo do arquivo JSON
    script_dir = Path(__file__).parent.parent  # Sobe um nível para a raiz do projeto
    json_path = script_dir / "instancias" / "ondina.json"
    
    if not json_path.exists():
        logger.error(f"Arquivo do grafo não encontrado em {json_path}")
        return
        
    grafo = load_graph_from_json(str(json_path))
    total_vertices = len(grafo.nodes())
    total_arestas = len(grafo.edges())
    logger.info(f"\nGrafo de Ondina carregado:")
    logger.info(f"- Total de vértices: {total_vertices}")
    logger.info(f"- Total de arestas: {total_arestas}")
        
    solver = CoberturaVertices(grafo)
    
    # Resolve cobertura completa
    cobertura_completa = solver.resolve_cobertura_completa()
    solver.salvar_resultado(cobertura_completa, "resultados/cobertura_completa.json")
    
    # Resolve cobertura máxima com limite de câmeras
    p = 40  # número máximo de câmeras
    cobertura_maxima, vertices_cobertos = solver.resolve_cobertura_maxima(p)
    solver.salvar_resultado(cobertura_maxima, "resultados/cobertura_maxima.json", vertices_cobertos)
    
    # Log dos resultados em formato similar ao README
    logger.info(f"\nResultados da execução:")
    logger.info("Cobertura Completa:")
    logger.info(f"- Necessita de {len(cobertura_completa)} câmeras para cobrir todos os {total_vertices} vértices")
    logger.info(f"- Média de {total_vertices/len(cobertura_completa):.1f} vértices cobertos por câmera")
    
    vertices_cobertos_max = len(vertices_cobertos)
    porcentagem_cobertura = (vertices_cobertos_max / total_vertices) * 100
    logger.info("\nCobertura Máxima:")
    logger.info(f"- Com {p} câmeras, consegue cobrir {vertices_cobertos_max} vértices ({porcentagem_cobertura:.1f}% do total)")
    logger.info(f"- Média de {vertices_cobertos_max/p:.1f} vértices cobertos por câmera")
    
    # Salva um resumo em formato markdown
    with open("resultados/README.md", "w") as f:
        f.write("## Resultados da Execução\n\n")
        f.write("Na execução com o grafo de Ondina:\n")
        f.write(f"- Total de vértices no grafo: {total_vertices}\n")
        f.write(f"- Total de arestas no grafo: {total_arestas}\n\n")
        f.write("### Cobertura Completa\n")
        f.write(f"- Necessita de {len(cobertura_completa)} câmeras para cobrir todos os {total_vertices} vértices\n")
        f.write(f"- Média de {total_vertices/len(cobertura_completa):.1f} vértices cobertos por câmera\n\n")
        f.write("### Cobertura Máxima\n")
        f.write(f"- Com {p} câmeras, consegue cobrir {vertices_cobertos_max} vértices ({porcentagem_cobertura:.1f}% do total)\n")
        f.write(f"- Média de {vertices_cobertos_max/p:.1f} vértices cobertos por câmera\n")

if __name__ == "__main__":
    main() 