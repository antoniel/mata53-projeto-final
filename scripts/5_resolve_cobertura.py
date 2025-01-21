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

    def resolve_cobertura_maxima(self, p: int) -> Tuple[Set[int], Set[int]]:
        """
        Implementa o algoritmo para cobertura máxima com número limitado de câmeras.
        Uma câmera instalada em um vértice cobre todos os vértices adjacentes
        e o próprio vértice.
        
        Args:
            p (int): Número máximo de câmeras permitidas
            
        Returns:
            Tuple[Set[int], Set[int]]: (conjunto de vértices selecionados, conjunto de vértices cobertos)
        """
        cobertura = set()
        vertices_cobertos = set()
        
        for _ in range(p):
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
            
        return cobertura, vertices_cobertos

    def salvar_resultado(self, cobertura: Set[int], arquivo_saida: str):
        """
        Salva o resultado da cobertura em um arquivo JSON.
        
        Args:
            cobertura (Set[int]): Conjunto de vértices selecionados
            arquivo_saida (str): Caminho do arquivo de saída
        """
        resultado = {
            "vertices_selecionados": list(cobertura),
            "num_cameras": len(cobertura),
            "cobertura_total": len(set().union(*[set(self.grafo.neighbors(v)) | {v} for v in cobertura])),
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
    logger.info(f"Grafo carregado com {len(grafo.nodes())} vértices e {len(grafo.edges())} arestas")
        
    solver = CoberturaVertices(grafo)
    
    # Resolve cobertura completa
    cobertura_completa = solver.resolve_cobertura_completa()
    solver.salvar_resultado(cobertura_completa, "resultados/cobertura_completa.json")
    
    # Resolve cobertura máxima com limite de câmeras
    p = 10  # número máximo de câmeras
    cobertura_maxima, vertices_cobertos = solver.resolve_cobertura_maxima(p)
    solver.salvar_resultado(cobertura_maxima, "resultados/cobertura_maxima.json")
    
    logger.info(f"Cobertura completa: {len(cobertura_completa)} câmeras")
    logger.info(f"Cobertura máxima com {p} câmeras: {len(vertices_cobertos)} vértices cobertos")

if __name__ == "__main__":
    main() 