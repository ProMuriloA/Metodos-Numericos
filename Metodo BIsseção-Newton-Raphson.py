import sys
import math
import re


def converter_potencia(expressao_str):
    """
    Converte expressões de potência como 'x^2' ou 'x²' para 'x**2'.
    """
    # Converte "x²" para "x**2"
    expressao_str = expressao_str.replace('²', '**2')
    expressao_str = expressao_str.replace('³', '**3')

    # Converte "x^2" para "x**2"
    expressao_str = re.sub(r'x\^(\d+)', r'x**\1', expressao_str)

    # Converte "2^3" para "2**3"
    expressao_str = re.sub(r'(\d+)\^(\d+)', r'\1**\2', expressao_str)

    return expressao_str


def string_para_funcao(expressao: str):
    """
    Converte uma string de expressão matemática em uma função Python executável.
    """
    ambiente = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'asinh': math.asinh, 'acosh': math.acosh, 'atanh': math.atanh,
        'log': math.log, 'log10': math.log10, 'log2': math.log2,
        'exp': math.exp, 'sqrt': math.sqrt, 'abs': abs, 'fabs': math.fabs,
        'pi': math.pi, 'e': math.e, 'tau': math.tau,
        'degrees': math.degrees, 'radians': math.radians
    }

    def f(x):
        ambiente_local = {**ambiente, 'x': x}
        try:
            return eval(expressao, {'__builtins__': None}, ambiente_local)
        except Exception as e:
            print(f"Erro ao avaliar função em x={x}: {e}")
            return float('nan')

    return f


# Solicitar a função do usuário
funcao_str = input("Digite a função f(x) (use 'x' como variável, ex: x**2 - 2): ")

# Converter notações alternativas de potência
funcao_str = converter_potencia(funcao_str)
print(f"Expressão convertida: {funcao_str}")

# Criar a função matemática
funcao = string_para_funcao(funcao_str)


# Derivada numérica com diferenças centrais
def derivada(x, h=1e-5):
    return (funcao(x + h) - funcao(x - h)) / (2 * h)


def bissecao_newton_raphson(a, b):
    # Configurações
    TOL_BISSEC = 1e-8
    TOL_NEWTON = 1e-15
    MAX_ITER_BISSEC = 100
    MAX_ITER_TOTAL = 200

    # Avalia a função nos pontos iniciais
    fa = funcao(a)
    fb = funcao(b)

    # Verifica se há troca de sinal
    if fa * fb >= 0:
        print("O método da bisseção falha. Certifique-se de que f(a) e f(b) têm sinais opostos.")
        print(f"f(a) = {fa}, f(b) = {fb}")
        return None

    iteracao = 0
    c = (a + b) / 2

    # Fase de Bissecção
    while iteracao < MAX_ITER_BISSEC:
        c = (a + b) / 2
        fc = funcao(c)

        # Verifica erros na função
        if math.isnan(fc):
            print("Valor inválido encontrado na função. Interrompendo cálculo.")
            return None

        print(f"Iteração {iteracao + 1} (Bisseção): a = {a:.16e}, b = {b:.16e}, c = {c:.16e}, f(c) = {fc:.16e}")

        # Critério de convergência
        if abs(fc) < TOL_BISSEC:
            print(f"Bisseção convergiu após {iteracao + 1} iterações")
            return c

        # Atualizar intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        # Critério de parada
        if abs(b - a) < TOL_BISSEC:
            print(f"Intervalo suficientemente pequeno após {iteracao + 1} iterações de bisseção")
            break

        iteracao += 1
    else:
        print("Máximo de iterações da bisseção atingido.")

    # Fase de Newton-Raphson
    x = c
    print(f"\nIniciando Newton-Raphson com x0 = {x:.16e}")
    newton_iter = 0

    while newton_iter < MAX_ITER_TOTAL - iteracao:
        fx = funcao(x)
        dfx = derivada(x)

        # Tratar derivada zero
        if abs(dfx) < 1e-15:
            print("Derivada muito próxima de zero. Retornando melhor estimativa.")
            return x

        x_new = x - fx / dfx
        fx_new = funcao(x_new)
        newton_iter += 1
        print(f"Iteração {iteracao + newton_iter} (Newton-Raphson): x = {x_new:.16e}, f(x) = {fx_new:.16e}")

        # Critérios de convergência
        if abs(fx_new) < TOL_NEWTON or abs(x_new - x) < TOL_NEWTON:
            print("Convergência alcançada.")
            x = x_new
            break

        x = x_new
    else:
        print("Máximo de iterações total atingido.")

    print(f"\nRaiz aproximada após {iteracao + newton_iter} iterações: {x:.16e}")
    return x


# Entrada do intervalo
a = float(input("Digite o valor inicial do intervalo (a): "))
b = float(input("Digite o valor final do intervalo (b): "))

# Executa o método híbrido
raiz = bissecao_newton_raphson(a, b)
if raiz is not None:
    print(f"A raiz encontrada é: {raiz:.16e}")