from pyomo.environ import *

def solve_optimization_problem(objective, constraints):
    model = ConcreteModel()

    # Variables (assuming variables are x1, x2, ...)
    model_vars = {var: Var(within=NonNegativeReals) for var in objective.keys()}
    for var, var_obj in model_vars.items():
        setattr(model, var, var_obj)

    # Objective function
    model.obj = Objective(expr=sum(coef * model_vars[var] for var, coef in objective.items()), sense=maximize)

    # Constraints
    constraint_count = 1
    for name, constraint in constraints.items():
        expr = sum(coef * model_vars[var] for var, coef in constraint.items() if var != "rhs")
        rhs = constraint["rhs"]
        constraint_obj = Constraint(expr=(expr <= rhs))
        setattr(model, f"constraint{constraint_count}", constraint_obj)
        constraint_count += 1

    # Solver
    solver = SolverFactory('glpk')
    result = solver.solve(model)

    # Collect results
    results = {
        "objective_value": model.obj(),
        "variables": {var: model_vars[var].value for var in model_vars},
        "constraints": {name: getattr(model, name)() for name in model.component_map(Constraint)}
    }

    return results