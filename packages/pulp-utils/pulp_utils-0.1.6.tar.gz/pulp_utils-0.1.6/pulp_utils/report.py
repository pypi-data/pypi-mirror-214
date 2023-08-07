from pulp import LpStatus
import numpy as np

__all__ = ['report_result', 'report_tsp_result']


def report_result(model):
    """
    Utility function to simplify PuLP result parsing
    """
    result = {
        "solver": model.solver.name,
        "optimization_result": {
            model.objective.name: model.objective.value(),
            "status": LpStatus[model.status]
        },
        "constraint_sensitivity": [
            {'name': name, 'constraint': str(c), 'activity': c.value() - c.constant, 'slack': c.slack}
            if model.isMIP() else 
            {'name': name, 'constraint': str(c), 'marginal': c.pi, 'activity': c.value() - c.constant, 'slack': c.slack}
            for name, c in model.constraints.items()
        ]
    }
    for v in model.variables(): 
        result["optimization_result"][v.name] = v.varValue
    return result


def report_tsp_result(model, x=None):
    """
    Utility function to simplify PuLP-Utils LpTSP result parsing
    """
    if x is None:
        x = model.vars
        
    N = x.shape[0]
    x_val = np.reshape([i.value() for i in x.flatten()], x.shape)
    dest_id = x_val.argmax(1)
    start = x_val.argmax(0)[0]

    route = [dest_id[start]]
    for _ in range(1, N+1):
        route.append(dest_id[route[-1]])
    
    
    result = {
        "solver": model.solver.name,
        "optimization_result": {
            model.objective.name: model.objective.value(),
            "status": LpStatus[model.status],
            "route": route,
            "x": x_val.astype(int)
        }
    }
    return result
