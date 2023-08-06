import time
import numpy as np
from pathlib import Path
import pickle

class Genetic:
    __slots__ = [
        "functions",
        "gene_space",
        "initial_population",
        "stop_time",
        "saving_path",
        "cpt_loop",
        "seed",
        "multiprocessing"
    ]

    def __init__(
        self,
        functions,
        gene_space: list,
        initial_population: np.ndarray,  # one line = one chromosome !!!
        stop_time: int,  # in seconds
        saving_path: str,
        seed: int,
        multiprocessing: bool
    ):
        self.functions = functions
        self.gene_space = gene_space
        self.initial_population = initial_population
        self.stop_time = stop_time
        self.saving_path = saving_path
        Path(saving_path).mkdir(parents=True, exist_ok=True)
        self.cpt_loop = 0
        self.seed = seed
        np.random.seed(seed)
        self.multiprocessing = multiprocessing

    def run(self):
        start_time = time.time()

        population = self.initial_population

        current_time = time.time()
        while (current_time - start_time) <= self.stop_time:
            print(f"Loop {self.cpt_loop}:")
            loop_start_time = time.time()

            costs = self.functions.evaluate(self, population)
            parents, costs_parents = self.functions.select_parents(self, population, costs)
            print(f"\tBest parent: {list(parents[0])[:5]}")
            print(f"\tBest 5 parents costs: {costs_parents[0:5]}")
            crossover_offspring = self.functions.crossover(self, parents, costs_parents)
            mutations_from_parents, mutations_from_crossover_offspring = self.functions.mutate(
                self, parents, crossover_offspring
            )

            data_to_save = {
                "cpt_loop": self.cpt_loop,
                "population": population,
                "costs": costs,
                "parents": parents,
                "costs_parents": costs_parents,
                "crossover_offspring": crossover_offspring,
                "mutations_from_parents": mutations_from_parents,
                "mutations_from_crossover_offspring": mutations_from_crossover_offspring,
            }
            with open(f"{self.saving_path}/loop_{self.cpt_loop}.pkl", "wb") as handle:
                pickle.dump(data_to_save, handle, protocol=pickle.HIGHEST_PROTOCOL)

            population = self.functions.create_new_population(
                self,
                parents,
                crossover_offspring,
                mutations_from_parents,
                mutations_from_crossover_offspring,
            )

            current_time = time.time()
            print(
                f"\tTime of loop {self.cpt_loop}: {np.round(current_time - loop_start_time, 2)} seconds"
            )
            self.cpt_loop += 1
