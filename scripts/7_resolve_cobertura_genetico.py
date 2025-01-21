#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
from typing import List, Set, Tuple
import json
import random
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_graph_from_json(json_path: str) -> nx.Graph:
    """
    Carrega o grafo a partir do arquivo JSON.
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    G = nx.Graph()
    
    # Adiciona nós
    for node in data['nodes']:
        G.add_node(
            node['id'],
            lat=node['lat'],
            lon=node['lon']
        )
    
    # Adiciona arestas
    for edge in data['edges']:
        G.add_edge(
            edge['source'],
            edge['target'],
            weight=edge['weight'],
            name=edge.get('name', '')
        )
    
    return G

class GeneticVertexCover:
    def __init__(self, graph, population_size=1000, generations=200, crossover_rate=0.8, mutation_rate=0.1):
        self.graph = graph
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_cameras = 40  # Limitando a 40 câmeras
        self.best_solution = None
        self.best_fitness = float('-inf')
        
    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            # Gera um indivíduo com exatamente 40 câmeras
            individual = [0] * len(self.graph.nodes())
            camera_positions = random.sample(range(len(individual)), self.max_cameras)
            for pos in camera_positions:
                individual[pos] = 1
            population.append(individual)
        return population
    
    def calculate_fitness(self, individual):
        cameras = [i for i, gene in enumerate(individual) if gene == 1]
        if len(cameras) > self.max_cameras:  # Penaliza soluções com mais de 40 câmeras
            return float('-inf')
            
        vertices_cobertos = set()
        for camera in cameras:
            vertices_cobertos.add(camera)
            vertices_cobertos.update(self.graph.neighbors(camera))
            
        return len(vertices_cobertos)
    
    def crossover(self, parent1, parent2):
        if random.random() > self.crossover_rate:
            return parent1, parent2
            
        point = random.randint(1, len(parent1)-1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        
        # Ajusta para manter exatamente 40 câmeras
        for child in [child1, child2]:
            cameras = sum(child)
            while cameras != self.max_cameras:
                if cameras < self.max_cameras:
                    zeros = [i for i, gene in enumerate(child) if gene == 0]
                    if zeros:
                        pos = random.choice(zeros)
                        child[pos] = 1
                        cameras += 1
                else:
                    ones = [i for i, gene in enumerate(child) if gene == 1]
                    if ones:
                        pos = random.choice(ones)
                        child[pos] = 0
                        cameras -= 1
                        
        return child1, child2
    
    def mutate(self, individual):
        if random.random() > self.mutation_rate:
            return individual
            
        # Troca uma câmera de posição
        ones = [i for i, gene in enumerate(individual) if gene == 1]
        zeros = [i for i, gene in enumerate(individual) if gene == 0]
        
        if ones and zeros:
            remove_pos = random.choice(ones)
            add_pos = random.choice(zeros)
            individual[remove_pos] = 0
            individual[add_pos] = 1
            
        return individual
    
    def run(self):
        population = self.initialize_population()
        best_ever_fitness = float('-inf')
        best_ever_solution = None
        
        for generation in range(self.generations):
            # Avalia a população
            fitness_scores = [(self.calculate_fitness(ind), ind) for ind in population]
            fitness_scores.sort(reverse=True)
            
            # Atualiza a melhor solução
            current_best_fitness = fitness_scores[0][0]
            if current_best_fitness > best_ever_fitness:
                best_ever_fitness = current_best_fitness
                best_ever_solution = fitness_scores[0][1].copy()  # importante fazer uma cópia
                print(f"Geração {generation}: Melhor fitness = {best_ever_fitness}")
            
            self.best_fitness = best_ever_fitness
            self.best_solution = best_ever_solution
            
            # Seleção
            new_population = []
            elite_size = 2
            new_population.extend([ind for _, ind in fitness_scores[:elite_size]])
            
            # Crossover e Mutação
            while len(new_population) < self.population_size:
                parent1 = random.choice([ind for _, ind in fitness_scores[:50]])
                parent2 = random.choice([ind for _, ind in fitness_scores[:50]])
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.extend([child1, child2])
            
            population = new_population[:self.population_size]
        
        return self.best_solution
    
    def get_coverage(self):
        if not self.best_solution:
            return None
            
        cameras = [i for i, gene in enumerate(self.best_solution) if gene == 1]
        vertices_cobertos = set()
        for camera in cameras:
            vertices_cobertos.add(camera)
            vertices_cobertos.update(self.graph.neighbors(camera))
            
        return {
            'vertices_selecionados': list(cameras),
            'vertices_cobertos': list(vertices_cobertos),
            'total_cameras': len(cameras),
            'total_cobertura': len(vertices_cobertos),
            'total_vertices': len(self.graph.nodes())
        }

def main():
    # Carregar o grafo
    script_dir = Path(__file__).parent.parent
    json_path = script_dir / "instancias" / "ondina.json"
    resultados_dir = script_dir / "resultados"
    
    print("Carregando grafo...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    G = nx.Graph()
    for node in data['nodes']:
        G.add_node(node['id'])
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'])
    
    print(f"Grafo carregado: {len(G.nodes())} vértices, {len(G.edges())} arestas")
    
    # Executar o algoritmo genético
    print("\nExecutando algoritmo genético...")
    ga = GeneticVertexCover(G)
    solution = ga.run()
    coverage = ga.get_coverage()
    
    # Salvar resultados
    os.makedirs(resultados_dir, exist_ok=True)
    output_path = resultados_dir / "ga_cobertura_ondina.json"
    
    with open(output_path, 'w') as f:
        json.dump(coverage, f, indent=2)
    
    print(f"\nResultados salvos em {output_path}")
    print(f"Câmeras utilizadas: {coverage['total_cameras']}")
    print(f"Vértices cobertos: {coverage['total_cobertura']} de {coverage['total_vertices']}")
    print(f"Média de vértices por câmera: {coverage['total_cobertura']/coverage['total_cameras']:.2f}")

if __name__ == "__main__":
    main() 