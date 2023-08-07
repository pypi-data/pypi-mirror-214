import numpy as np
from pulp import LpProblem, LpVariable, lpSum

__all__ = ['LpSupplyDemand']


class LpSupplyDemand(LpProblem):
    """
    Extension of LpProblem to quickly define a simple Supply-Demand LP Problem

    ====== Input ======
    name: str
        name of the problem used in the output .lp file

    sense: {LpMaximize, LpMinimize}
        sense of the LP problem objective

    supply: dict
        key-value pair for the supply. Example:
        supply = {"K": 400000, "L": 300000, "M": 200000}

    demand: dict
        key-value pair for the supply. Example:
        demand = {"A": 75000, "B": 150000, "C": 250000, "D": 300000}

    cost: np.array, list of list
        cost table for the supply to reach the demand.
        Should have the shape of (n_supply, n_demand)


    ====== Return ======
    PuLP LpProblem model


    ====== Example Usage ======
    from pulp import LpMinimize, PULP_CBC_CMD
    from pulp_utils import LpSupplyDemand, report_result

    supply = {
        "K": 400000,
        "L": 300000,
        "M": 200000    
    }

    demand = {
        "A": 75000,
        "B": 150000,
        "C": 250000,
        "D": 300000
    }

    cost = [
        [355000, 280000, 280000, 325000],
        [220000, 230000, 185000, 295000],
        [280000, 265000, 250000, 265000]    
    ]
    
    model = LpSupplyDemand("Sample_Name", LpMinimize, supply, demand, cost)
    model.solve(solver=PULP_CBC_CMD(msg=False))
    result = report_result(model)    
    """
    def __init__(self, name, sense, supply, demand, cost, mip=False, var_name="n", obj_name="cost", supply_name="supply", demand_name="demand"):
        super().__init__(name, sense)
        n_s, n_d = len(supply), len(demand)
        cost = np.array(cost)
        assert (n_s, n_d) == cost.shape

        self.supply = supply
        self.demand = demand
        self.cost = cost

        # Variables
        cat_val = "Integer" if mip else "Continuous"
        N = np.array([[LpVariable(f'{var_name}_{s}_{d}', 0, cat=cat_val) for d in demand.keys()] for s in supply.keys()])
        self.vars = N
        
        # Constraints
        self += (lpSum(N * cost), f"obj_{obj_name}")
        for i, (k, s) in enumerate(supply.items()):
            self += (lpSum(N[i, :]) <= s, f"C_{supply_name}_{k}")

        for i, (k, d) in enumerate(demand.items()):
            self += (lpSum(N[:, i]) >= d, f"C_{demand_name}_{k}")