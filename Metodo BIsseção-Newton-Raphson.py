import sys

def funcao(x):
    return x**3 + x**2 - x - 2

def derivada(x):
    return 3*x**2 + 2*x - 1

def bissecao_newton_raphson(a, b):
    if funcao(a) * funcao(b) >= 0:
        print("O método da bisseção falha. Certifique-se de que f(a) e f(b) têm sinais opostos.")
        return None

    iteracao = 0
    c = (a + b) / 2

    # Fase de Bissecção
    while True:
        c_prev = c
        c = (a + b) / 2
        print(f"Iteração {iteracao + 1} (Bisseção): a = {a:.16e}, b = {b:.16e}, c = {c:.16e}, f(c) = {funcao(c):.16e}")

        if funcao(c) == 0:
            print(f"A raiz exata é c = {c:.16e}")
            return c

        if funcao(a) * funcao(c) < 0:
            b = c
        else:
            a = c

        # Verifica se o próximo ponto médio não melhora a precisão
        next_c = (a + b) / 2
        if next_c == a or next_c == b or next_c == c_prev:
            print("Bisseção não pode reduzir mais o intervalo.")
            iteracao += 1
            break

        iteracao += 1

    # Fase de Newton-Raphson
    x = c
    print(f"Iniciando Newton-Raphson com x0 = {x:.16e}")
    while True:
        fx = funcao(x)
        dfx = derivada(x)

        if dfx == 0:
            print("Derivada zero encontrada. O método de Newton-Raphson falha.")
            return None

        x_new = x - fx / dfx
        print(f"Iteração {iteracao} (Newton-Raphson): x = {x_new:.16e}, f(x) = {funcao(x_new):.16e}")

        # Verifica convergência na precisão da máquina
        if x_new == x:
            print("Convergência alcançada (sem mudança em x).")
            break

        x = x_new
        iteracao += 1

    print(f"Raiz aproximada após {iteracao} iterações: {x:.16e}")
    return x

# Configuração automática para precisão máxima
tolerancia = sys.float_info.epsilon

# Entrada do usuário
a = float(input("Digite o valor inicial do intervalo (a): "))
b = float(input("Digite o valor final do intervalo (b): "))

# Executa o método híbrido
raiz = bissecao_newton_raphson(a, b)
if raiz is not None:
    print(f"A raiz encontrada é: {raiz:.16e}")
