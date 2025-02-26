def funcao(x):
    # Define the function for which you want to find the root
    return x**3 - x - 2  # Example: f(x) = x^3 - x - 2

def derivada(x):
    # Define the derivative of the function
    return 3*x**2 - 1  # Example: f'(x) = 3x^2 - 1

def bissecao_newton_raphson(a, b, tolerancia):
    # Step 1: Bisection to get close to the root
    if funcao(a) * funcao(b) >= 0:
        print("O método da bisseção falha. Certifique-se de que f(a) e f(b) têm sinais opostos.")
        return None

    iteracao = 0
    c = (a + b) / 2  # Initial midpoint
    while (b - a) / 2 > tolerancia:
        c = (a + b) / 2
        print(f"Iteração {iteracao + 1} (Bisseção): a = {a}, b = {b}, c = {c}, f(c) = {funcao(c)}")

        if funcao(c) == 0:  # Exact root found
            print(f"A raiz exata é c = {c}")
            return c
        elif funcao(a) * funcao(c) < 0:
            b = c
        else:
            a = c

        iteracao += 1

    # Step 2: Switch to Newton-Raphson for faster convergence
    x = c  # Use the bisection result as the initial guess for Newton-Raphson
    while abs(funcao(x)) > tolerancia:
        if derivada(x) == 0:
            print("Derivada zero encontrada. O método de Newton-Raphson falha.")
            return None

        x = x - funcao(x) / derivada(x)
        iteracao += 1
        print(f"Iteração {iteracao} (Newton-Raphson): x = {x}, f(x) = {funcao(x)}")

    print(f"Raiz aproximada após {iteracao} iterações: {x}")
    return x

# Input parameters
a = float(input("Digite o valor inicial do intervalo (a): "))
b = float(input("Digite o valor final do intervalo (b): "))
tolerancia = float(input("Digite a tolerância para a precisão da raiz: "))

# Execute the hybrid method
raiz = bissecao_newton_raphson(a, b, tolerancia)
if raiz is not None:
    print(f"A raiz encontrada é: {raiz}")
