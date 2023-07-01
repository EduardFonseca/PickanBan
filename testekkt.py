import numpy as np
import sympy as sym

def kkt_conditions(X, f, r):
    """
    Verifica se o ponto (x, y) satisfaz as condições KKT para o problema de otimização.

    CONDIÇÕES DE KKT
    1. grad(f(x)) + lambda*grad(g(x)) = 0

    onde:
        g(x) <= 0
        lambda >= 0
        lambda*g(x) = 0


    Args:
        X: Valor a ser verificado.
        f: A função objetivo [minimização].
        r: A lista de restrições [<=0].

    Returns:
        True se o ponto satisfaz as condições KKT, False caso contrário.
    """

    fob = sym.sympify(f)
    constraints = [sym.sympify(i) for i in r]

    variables = list(fob.free_symbols)
    
    # ordena as variáveis
    variables.sort(key=lambda x: x.name)
    og_variables = variables.copy()

    # cria uma lista de lambdas para cada restrição
    lambdas = [sym.symbols(f"lambda{i+1}") for i in range(len(constraints))]
    lambdas.sort(key=lambda x: x.name)

    # Cria a função lagrangiana
    lagrangiana = fob
    for i in range(len(constraints)):
        lagrangiana += lambdas[i]*constraints[i]

    print(lagrangiana)

    # Calcula o gradiente da lagrangiana
    lagrangiana = sym.Matrix([lagrangiana])

    sistema = lagrangiana.jacobian(variables)

    # substitui os valores de x no sistema de equações
    sistema = sistema.subs({og_variables[0]: X[0], og_variables[1]: X[1]})

    # Calcula os valores de lambda para o sistema = 0 #TODO: Melhorar isso
    listas = []
    for equacao in sistema:
        listas.append(equacao)

    valores_lambda = sym.solve(listas, lambdas)
    
    # Verifica se os valores de lambda são >= 0
    for valor in valores_lambda.values():
        if valor < 0:
            print("λ < 0")
            return False
    
    # Verifica se G(x) <= 0
    vals = []
    for restricao in constraints:
        aux = restricao.subs({og_variables[0]: X[0], og_variables[1]: X[1]})
        if abs(aux) < 1e-15:
            aux = 0
        vals.append(aux)
        if vals[-1] > 0:
            print("g(x) > 0")
            return False

    # Verifica se lambda*g(x) = 0
    for i in range(len(vals)):
        if vals[i]*valores_lambda[lambdas[i]] != 0:
            print("λg(x) ≠ 0")
            return False
 
    # Verifica se grad(f(x)) + lambda*grad(g(x)) = 0

    # grad(f(x))
    grad_f = sym.Matrix([fob]).jacobian(variables)

    # grad(g(x))
    grad_g = sym.Matrix(constraints).jacobian(variables)

    # Transforma o dict em uma lista
    lambda_val = []
    for val in valores_lambda.values():
        lambda_val.append(val)
    lambda_val = sym.Matrix(lambda_val).transpose()

    resultado = grad_f + lambda_val*grad_g

    # Verifica se o resultado é 0
    for i in range(len(resultado)):
        if abs(resultado[i]) > 1e-15:
            return False

    return True


def main():
    # x = 0
    # y = 2
    x = np.float64(4/3)
    y = np.float64(8/3)
    
    ponto = [x, y]
    fob = "-x1 - 3*x2"
    restricoes = ["-x1 + 2*x2 - 4", "x1 + x2 - 4"]

    if kkt_conditions(ponto, fob, restricoes):
        print(f"O ponto [x, y] = [{x},{y}] satisfaz as condições KKT.")
    else:
        print(f"O ponto [x, y] = [{x},{y}] não satisfaz as condições KKT.")

if __name__ == "__main__":
    main()
