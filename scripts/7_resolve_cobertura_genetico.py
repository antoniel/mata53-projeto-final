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
    def __init__(
        self,
        grafo: nx.Graph,
        population_size: int = 50,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.01,
        generations: int = 100,
        penalty_factor: int = 100
    ):
        """
        Inicializa o algoritmo genético para o problema de cobertura de vértices.
        
        Args:
            grafo (nx.Graph): Grafo do NetworkX.
            population_size (int): Tamanho da população (número de indivíduos).
            crossover_rate (float): Probabilidade de ocorrer crossover.
            mutation_rate (float): Probabilidade de mutação de cada bit.
            generations (int): Número de gerações a evoluir.
            penalty_factor (int): Fator de penalização para vértices não cobertos.
        """
        self.grafo = grafo
        self.num_vertices = grafo.number_of_nodes()
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.penalty_factor = penalty_factor

        # Lista de vizinhos (para agilizar cálculo de cobertura)
        self.neighbors_list = []
        for v in range(self.num_vertices):
            # Garante que a ordem dos nós é de 0..n-1
            # Se o seu grafo possui rótulos diferentes, você pode mapear para [0..n-1].
            self.neighbors_list.append(list(self.grafo.neighbors(v)))
        
        # População: cada indivíduo é uma lista/array binária de tamanho num_vertices
        self.population = []
        self.best_individual = None
        self.best_fitness = float('-inf')
        
    def _initialize_population(self):
        """
        Gera a população inicial de forma aleatória.
        """
        self.population = []
        for _ in range(self.population_size):
            # Cria uma string binária/ lista de 0,1 aleatória
            individual = [random.randint(0,1) for _ in range(self.num_vertices)]
            self.population.append(individual)
    
    def _fitness(self, individual: List[int]) -> float:
        """
        Calcula o valor de fitness de um indivíduo (quanto maior melhor).
        
        - Verifica se todos os vértices estão cobertos: 
            Vértice v coberto se individual[v] == 1 OU 
            algum de seus vizinhos está == 1.
        - Se algum vértice não estiver coberto, adiciona penalidade.
        - Caso todos estejam cobertos, recompensa soluções com menos câmeras.
        """
        uncovered_vertices = 0
        for v in range(self.num_vertices):
            if individual[v] == 1:
                continue  # se esse vértice tem câmera, ele próprio está coberto
            else:
                # se não tem câmera, checa se algum vizinho tem
                vizinhos = self.neighbors_list[v]
                # se nenhum dos vizinhos tiver câmera, então v não está coberto
                if not any(individual[n] == 1 for n in vizinhos):
                    uncovered_vertices += 1
        
        num_cameras = sum(individual)  # quantas câmeras foram colocadas
        
        if uncovered_vertices == 0:
            # Todos os vértices estão cobertos
            # Fitness maior para soluções com menos câmeras
            # Ex: fitness = 1 / (1 + num_cameras)
            return 1.0 / (1.0 + num_cameras)
        else:
            # Penaliza soluções que não cobrem todos
            # Ex: fitness = 1 / (1 + num_cameras + P*uncovered_vertices)
            return 1.0 / (1.0 + num_cameras + self.penalty_factor * uncovered_vertices)

    def _selection(self) -> List[int]:
        """
        Seleção por torneio (tamanho 2).
        Retorna um indivíduo (cópia) vencedor do torneio.
        """
        # Escolhe dois indivíduos aleatoriamente
        i1, i2 = random.sample(self.population, 2)
        f1 = self._fitness(i1)
        f2 = self._fitness(i2)
        
        if f1 > f2:
            return i1[:]
        else:
            return i2[:]
    
    def _crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Crossover de um ponto simples. Retorna dois filhos.
        """
        if random.random() < self.crossover_rate:
            point = random.randint(1, self.num_vertices - 1)
            # Faz o corte e troca de pedaços
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
        else:
            # Sem crossover, retorna os pais inalterados
            child1 = parent1[:]
            child2 = parent2[:]
        return child1, child2
    
    def _mutation(self, individual: List[int]):
        """
        Mutação simples: inverte bit com probabilidade mutation_rate.
        """
        for i in range(self.num_vertices):
            if random.random() < self.mutation_rate:
                individual[i] = 1 - individual[i]  # inverte o bit
    
    def run(self):
        """
        Executa o loop principal do algoritmo genético.
        """
        self._initialize_population()
        
        for generation in range(self.generations):
            new_population = []
            
            # Opcional: Elitismo - guarda o melhor indivíduo
            # Calcula fitness de toda população para achar o melhor
            current_best = None
            current_best_fitness = float('-inf')
            
            for ind in self.population:
                f = self._fitness(ind)
                if f > current_best_fitness:
                    current_best_fitness = f
                    current_best = ind
            
            # Se for melhor que global, atualiza
            if current_best_fitness > self.best_fitness:
                self.best_fitness = current_best_fitness
                self.best_individual = current_best[:]
            
            # Elitismo (mantenha o melhor na próxima geração)
            new_population.append(self.best_individual[:])
            
            # Gera nova população por seleção, crossover e mutação
            while len(new_population) < self.population_size:
                parent1 = self._selection()
                parent2 = self._selection()
                child1, child2 = self._crossover(parent1, parent2)
                self._mutation(child1)
                self._mutation(child2)
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)
            
            self.population = new_population
            
            if (generation+1) % 10 == 0:
                logger.info(f"Geração {generation+1}/{self.generations} | Melhor fitness: {self.best_fitness:.6f}")
        
        # Ao final, best_individual terá a melhor solução encontrada
        logger.info(f"GA finalizado! Melhor fitness obtido: {self.best_fitness:.6f}")
    
    def get_best_solution(self) -> Tuple[List[int], float]:
        """
        Retorna o melhor indivíduo (lista de bits) e sua fitness.
        """
        return self.best_individual, self.best_fitness
    
    def save_solution(self, output_path: str):
        """
        Salva a melhor solução encontrada em um arquivo JSON,
        incluindo quantos vértices foram selecionados e a cobertura resultante.
        """
        if self.best_individual is None:
            logger.warning("Nenhuma solução foi encontrada (best_individual == None).")
            return
        
        chosen_vertices = [i for i, bit in enumerate(self.best_individual) if bit == 1]
        
        # Verifica quantos vértices estão cobertos na prática
        covered_vertices = set()
        for v in range(self.num_vertices):
            if self.best_individual[v] == 1:
                covered_vertices.add(v)
                covered_vertices.update(self.neighbors_list[v])
        
        # Monta dicionário de resultado
        result = {
            "vertices_selecionados": chosen_vertices,
            "numero_cameras": len(chosen_vertices),
            "vertices_cobertos": list(covered_vertices),
            "numero_vertices_cobertos": len(covered_vertices),
            "total_vertices_no_grafo": self.num_vertices,
            "fitness": self.best_fitness
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)

def main():
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
    logger.info(f"- Total de arestas: {total_arestas}\n")
    
    # Parâmetros do algoritmo genético (ajuste conforme necessário)
    population_size = 50
    crossover_rate = 0.8
    mutation_rate = 0.01
    generations = 200
    penalty_factor = 100
    
    ga_solver = GeneticVertexCover(
        grafo=grafo,
        population_size=population_size,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        generations=generations,
        penalty_factor=penalty_factor
    )
    
    # Executa o GA
    ga_solver.run()
    
    # Obtém a melhor solução
    best_individual, best_fitness = ga_solver.get_best_solution()
    
    chosen_vertices = [i for i, bit in enumerate(best_individual) if bit == 1]
    logger.info(f"Melhor indivíduo: {chosen_vertices}")
    logger.info(f"Número de câmeras (vértices selecionados): {len(chosen_vertices)}")
    
    # Salva resultado em JSON
    ga_solver.save_solution(str(script_dir / "resultados" / "ga_cobertura_ondina.json"))

if __name__ == "__main__":
    main() 