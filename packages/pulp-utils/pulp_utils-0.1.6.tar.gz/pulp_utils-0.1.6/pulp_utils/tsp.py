from pulp import LpProblem, LpVariable, lpSum

import numpy as np
from scipy.spatial import distance_matrix
import matplotlib.pyplot as plt

__all__ = ["LpTSP", "SyntheticTSP"]


class LpTSP(LpProblem):
    """
    Extension of LpProblem to quickly define a simple TSP LP Problem based on MTZ Formulation.
    source: C. E. Miller, A. W. Tucker, and R. A. Zemlin. 1960. Integer Programming Formulation of Traveling Salesman Problems. J. ACM 7, 4 (Oct. 1960), 326–329.
    DOI: 10.1145/321043.321046

    ====== Input ======
    name: str
        name of the problem used in the output .lp file

    sense: {LpMaximize, LpMinimize}
        sense of the LP problem objective

    distances: np.array
        distance matrix


    ====== Return ======
    PuLP LpProblem model


    ====== Example Usage ======
    from pulp import LpMinimize, PULP_CBC_CMD
    from pulp_utils import LpTSP, report_tsp_result
    
    model = LpTSP("Sample_Name", LpMinimize, distances)
    model.solve(solver=PULP_CBC_CMD(msg=False))
    result = report_tsp_result(model)
    """
    def __init__(self, name, sense, distances, var_name="x", obj_name="total_distance"):
        super().__init__(name, sense)
        N, _ = distances.shape

        # Variables
        x = np.array([[LpVariable(f'{var_name}_{i}_{j}', cat="Binary") for j in range(N)] for i in range(N)])
        u = [LpVariable(f'u_{i}', 1, N, cat="Integer") for i in range(N-1)]
        self.vars = x

        # Constraints
        self += (lpSum(distances*x), f"obj_{obj_name}")
        for i in range(N):
            self += (x[i, i] == 0, f"C_must_move_{i}")
            self += (lpSum(x[i, :]) == 1, f"C_row_sum_{i}")
            self += (lpSum(x[:, i]) == 1, f"C_col_sum_{i}")
        
        for i in range(1, N):
            for j in range(1, N):
                if i != j:
                    self += (u[i-1] - u[j-1] + (N-1)*x[i, j] <= N - 2, f"C_avoid_subtour_{i}_{j}")


class SyntheticTSP():
    def __init__(self, n, random_state=42):
        state = np.random.RandomState(random_state)
        self.N = n
        self.locations = state.randint(0, 100, size=(n, 2))
        self.distances = distance_matrix(self.locations, self.locations)
        
    def plot(self):
        plot_tsp(self.locations)


def plot_tsp(locations, route=[], figsize=(5, 5), show_annotation=True, origin_name="depot"):
    N = len(locations)
    
    plt.figure(figsize=figsize)
    plt.scatter(locations[0, 0], locations[0, 1], s=40, c="r", marker="o")
    plt.scatter(locations[1:, 0], locations[1:, 1], s=20, c="b", marker="x")
    
    if show_annotation:
        for i in range(N):
            annot_text = origin_name if (i == 0) else i
            plt.text(locations[i, 0], locations[i, 1]+1, annot_text, ha="center")
    plt.axis('equal')
    plt.title(f"Traveling Salesman Problem (N={N})");
    
    for i, j in zip(route[:-1], route[1:]):
        start = (locations[i, 0], locations[i, 1])
        end = (locations[j, 0], locations[j, 1])
        arrowprops = dict(arrowstyle='->', connectionstyle='arc3', edgecolor='r')
        plt.annotate('', xy=end, xytext=start, arrowprops=arrowprops)