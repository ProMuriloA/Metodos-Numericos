def funcao(x):
    # Defina aqui a função para a qual deseja encontrar a raiz
    return x + 10  # Exemplo: raiz de x^3 - x - 2 = 0

def bissecao(a, b, tolerancia):
    if funcao(a) * funcao(b) >= 0:
        print("O método da bisseção falha. Certifique-se de que f(a) e f(b) têm sinais opostos.")
        return None

    iteracao = 0
    while (b - a) / 2 > tolerancia:
        c = (a + b) / 2
        print(f"Iteração {iteracao + 1}: a = {a}, b = {b}, c = {c}, f(c) = {funcao(c)}")

        if funcao(c) == 0:  # Encontrou a raiz exata
            print(f"A raiz exata é c = {c}")
            return c
        elif funcao(a) * funcao(c) < 0:
            b = c
        else:
            a = c

        iteracao += 1

    raiz_aproximada = (a + b) / 2
    print(f"Raiz aproximada após {iteracao} iterações: {raiz_aproximada}")
    return raiz_aproximada

# Parâmetros de entrada
a = float(input("Digite o valor inicial do intervalo (a): "))
b = float(input("Digite o valor final do intervalo (b): "))
tolerancia = float(input("Digite a tolerância para a precisão da raiz: "))

# Executa o método da bisseção
raiz = bissecao(a, b, tolerancia)
if raiz is not None:
    print(f"A raiz encontrada é: {raiz}")
