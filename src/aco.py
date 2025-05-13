import random
import math

class ACO:
    def __init__(self, distances, n_ants=10, n_iterations=50, alpha=1, beta=2, evaporation_rate=0.5, q=100):
        self.distances = distances  # Dictionnaire {(i, j): distance}
        self.nodes = list(set(i for i, j in distances.keys()))
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q  # constante de dépôt de phéromone

        # Initialisation des phéromones sur chaque arête
        self.pheromones = {(i, j): 1.0 for i, j in distances.keys()}

        # Liste pour stocker l'évolution de la distance
        self.distance_evolution = []

    def _heuristic(self, i, j):
        return 1.0 / self.distances[(i, j)]

    def _probability(self, current, unvisited):
        probabilities = []
        denom = sum(
            (self.pheromones[(current, j)] ** self.alpha) * (self._heuristic(current, j) ** self.beta)
            for j in unvisited
        )
        for j in unvisited:
            numer = (self.pheromones[(current, j)] ** self.alpha) * (self._heuristic(current, j) ** self.beta)
            probabilities.append((j, numer / denom))
        return probabilities

    def _select_next_node(self, current, unvisited):
        probs = self._probability(current, unvisited)
        r = random.random()
        total = 0.0
        for node, prob in probs:
            total += prob
            if r <= total:
                return node
        return unvisited[-1]  # fallback

    def _total_distance(self, path):
        return sum(self.distances[(path[i], path[i+1])] for i in range(len(path)-1))

    def run(self, start_node=0):
        best_path = []
        best_distance = float("inf")
        self.distance_evolution = []  # Réinitialise pour chaque exécution

        for iteration in range(self.n_iterations):
            all_paths = []
            all_distances = []

            for _ in range(self.n_ants):
                unvisited = [node for node in self.nodes if node != start_node]
                path = [start_node]

                while unvisited:
                    next_node = self._select_next_node(path[-1], unvisited)
                    path.append(next_node)
                    unvisited.remove(next_node)

                distance = self._total_distance(path)
                all_paths.append(path)
                all_distances.append(distance)

                if distance < best_distance:
                    best_distance = distance
                    best_path = path

            # Évaporation
            for edge in self.pheromones:
                self.pheromones[edge] *= (1 - self.evaporation_rate)

            # Dépôt de phéromone
            for path, distance in zip(all_paths, all_distances):
                for i in range(len(path) - 1):
                    edge = (path[i], path[i+1])
                    self.pheromones[edge] += self.q / distance

            # Ajoute la meilleure distance de cette itération
            self.distance_evolution.append(best_distance)

        return best_path, best_distance

    def get_distance_evolution(self):
        return self.distance_evolution