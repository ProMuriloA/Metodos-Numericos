import sys

# Solicitar apenas a função do usuário
funcao_str = input("Digite a função f(x) (use 'x' como variável, ex: x**2 - 2): ")

# Definir a função usando eval
funcao = lambda x: eval(funcao_str)

# Derivada numérica com diferenças centrais (precisão O(h²))
def derivada(x, h=1e-5):
    return (funcao(x + h) - funcao(x - h)) / (2 * h)

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

        # Verifica estagnação do intervalo
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

        if abs(dfx) < 1e-15:  # Evita divisão por zero
            print("Derivada muito próxima de zero. Método falha.")
            return None

        x_new = x - fx / dfx
        print(f"Iteração {iteracao} (Newton-Raphson): x = {x_new:.16e}, f(x) = {funcao(x_new):.16e}")

        if x_new == x:  # Convergência na precisão da máquina
            print("Convergência alcançada (sem mudança em x).")
            break

        x = x_new
        iteracao += 1

    print(f"Raiz aproximada após {iteracao} iterações: {x:.16e}")
    return x

# Entrada do intervalo
a = float(input("Digite o valor inicial do intervalo (a): "))
b = float(input("Digite o valor final do intervalo (b): "))

# Execução
raiz = bissecao_newton_raphson(a, b)
if raiz is not None:
    print(f"A raiz encontrada é: {raiz:.16e}")
