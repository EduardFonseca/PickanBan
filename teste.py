import numpy as np
import sympy as sym

def kkt_conditions(X, f, r):
    """
    Checks if the point (x, y) satisfies the KKT conditions for the optimization problem.

    CONDIÇÕES DE KKT
    1. grad(f(x)) + lambda*grad(g(x)) = 0

    onde:
        g(x) <= 0
        lambda >= 0
        lambda*g(x) = 0


    Args:
        X: Value to be checked.
        f: The objective function [minimization].
        r: The list of constraints [<=0].

    Returns:
        True if the point satisfies the KKT conditions, False otherwise.
    """

    fob = sym.sympify(f)
    constraints = [sym.sympify(i) for i in r]

    variables = list(fob.free_symbols)
    
    # order the variables
    variables.sort(key=lambda x: x.name)
    og_variables = variables.copy()

    # create a list of lambdas for each constraint
    lambdas = [sym.symbols(f"lambda{i+1}") for i in range(len(constraints))]
    lambdas.sort(key=lambda x: x.name)

    # Create the lagrangian function
    lagrangian = fob
    for i in range(len(constraints)):
        lagrangian += lambdas[i]*constraints[i]

    print(lagrangian)

    # Calculate the gradient of the lagrangian
    lagrangian = sym.Matrix([lagrangian])

    system = lagrangian.jacobian(variables)

    # sub x in for evry variable in og_variables
    system = system.subs({og_variables[0]: X[0], og_variables[1]: X[1]})

    # Calculate the values of lambda so system = 0 #TODO: Melhoar isso
    lists = []
    for equation in system:
        lists.append(equation)

    lambda_values = sym.solve(lists, lambdas)
    


    # Check if the values of lambda are >= 0
    for value in lambda_values.values():
        if value < 0:
            print("λ < 0")
            return False
    
    # Check if G(x) <= 0
    vals = []
    for constraint in constraints:
        aux = constraint.subs({og_variables[0]: X[0], og_variables[1]: X[1]})
        if abs(aux) < 1e-15:
            aux = 0
        vals.append(aux)
        if vals[-1] > 0:
            print("g(x) > 0")
            return False

    # Check if lambda*g(x) = 0
    for i in range(len(vals)):
        if vals[i]*lambda_values[lambdas[i]] != 0:
            print("λg(x) ≠ 0")
            return False
 
    # Check if grad(f(x)) + lambda*grad(g(x)) = 0

    # grad(f(x))
    grad_f = sym.Matrix([fob]).jacobian(variables)

    # grad(g(x))
    grad_g = sym.Matrix(constraints).jacobian(variables)

    # Transforma o dict em uma lista
    lambda_val = []
    for val in lambda_values.values():
        lambda_val.append(val)
    lambda_val = sym.Matrix(lambda_val).transpose()

    result = grad_f + lambda_val*grad_g

    # Check if result is 0
    for i in range(len(result)):
        if abs(result[i]) > 1e-15:
            return False

    return True


def main():
    x = 0
    y = 2
    # x = 4/3
    # y = 8/3

    point = [x, y]
    fob = "-x1 - 3*x2"
    constraints = ["-x1 + 2*x2 - 4", "x1 + x2 - 4"]

    if kkt_conditions(point, fob, constraints):
        print(f"The point [x, y] = [{x},{y}] satisfies the KKT conditions.")
    else:
        print(f"The point [x, y] = [{x},{y}] does not satisfy the KKT conditions.")

if __name__ == "__main__":
    main()
