import sys
import math
import re

def converter_potencia(expressao_str):
    """Converte notações de potência para sintaxe Python"""
    # Unicode exponents
    substituicoes_unicode = {
        '²': '**2', '³': '**3', '⁴': '**4', '⁵': '**5', 
        '⁶': '**6', '⁷': '**7', '⁸': '**8', '⁹': '**9', '⁰': '**0'
    }
    for char, repl in substituicoes_unicode.items():
        expressao_str = expressao_str.replace(char, repl)
    
    # Circumflex notation
    expressao_str = re.sub(r'(\d*\.?\d+|\b\w+|[\)])\s*\^\s*(\d*\.?\d+|\b\w+|[\()])', r'\1**\2', expressao_str)
    
    # Implicit multiplication
    expressao_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expressao_str)
    expressao_str = re.sub(r'([a-zA-Z\)])(\d)', r'\1*\2', expressao_str)
    
    return expressao_str

def string_para_funcao(expressao: str):
    """Converte string para função executável"""
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

def encontrar_intervalo(f):
    """Encontra automaticamente intervalo com troca de sinal"""
    pontos_teste = [-10, -5, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 3, 5, 10]
    print("Procurando intervalo com troca de sinal...")
    
    valores_validos = []
    for x in pontos_teste:
        try:
            fx = f(x)
            if not math.isnan(fx):
                print(f"f({x:.2f}) = {fx:.6e}")
                valores_validos.append((x, fx))
        except:
            continue
    
    for i in range(len(valores_validos)):
        x1, f1 = valores_validos[i]
        for j in range(i+1, len(valores_validos)):
            x2, f2 = valores_validos[j]
            if f1 * f2 < 0:
                print(f"\nTroca de sinal encontrada entre {x1:.2f} e {x2:.2f}")
                print(f"f({x1:.2f}) = {f1:.6e}")
                print(f"f({x2:.2f}) = {f2:.6e}")
                return min(x1, x2), max(x1, x2)
    
    raise ValueError("Não foi possível encontrar intervalo com troca de sinal automaticamente.")

# Solicitar a função do usuário
funcao_str = input("\nDigite a função f(x) (use 'x' como variável, ex: x**2 - 2): ")

# Converter notações de potência
funcao_str_convertida = converter_potencia(funcao_str)
print(f"Expressão convertida: {funcao_str_convertida}")

# Criar função matemática
funcao = string_para_funcao(funcao_str_convertida)

# Testar a função
print("\nTestando função em vários pontos:")
try:
    a, b = encontrar_intervalo(funcao)
    print(f"\nUsando intervalo automático: [{a:.2f}, {b:.2f}]")
except ValueError as e:
    print(e)
    print("\nPor favor, insira manualmente um intervalo onde a função troca de sinal.")
    a = float(input("Digite o valor inicial do intervalo (a): "))
    b = float(input("Digite o valor final do intervalo (b): "))

# Derivada numérica
def derivada(x, h=1e-5):
    return (funcao(x + h) - funcao(x - h)) / (2 * h)

def bissecao_newton_raphson(a, b):
    # Configurações
    TOL_BISSEC = 1e-8
    TOL_NEWTON = 1e-15
    MAX_ITER_BISSEC = 100
    MAX_ITER_TOTAL = 200
    
    # Avaliar função nos pontos iniciais
    fa = funcao(a)
    fb = funcao(b)
    
    # Verificar troca de sinal
    if math.isnan(fa) or math.isnan(fb):
        print("Valor inválido na função. Verifique o intervalo.")
        return None
        
    if fa * fb >= 0:
        print("ERRO: f(a) e f(b) devem ter sinais opostos!")
        print(f"f({a}) = {fa}")
        print(f"f({b}) = {fb}")
        return None

    iteracao = 0

    # Fase de Bissecção
    print("\nFase de Bissecção:")
    while iteracao < MAX_ITER_BISSEC:
        c = (a + b) / 2
        fc = funcao(c)
        
        if math.isnan(fc):
            print("Valor inválido encontrado na função.")
            return None
            
        print(f"Iteração {iteracao + 1}: a = {a:.6f}, b = {b:.6f}, c = {c:.6f}, f(c) = {fc:.6e}")

        if abs(fc) < TOL_BISSEC:
            print(f"Convergência na bisseção após {iteracao+1} iterações")
            return c

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        if abs(b - a) < TOL_BISSEC:
            print(f"Intervalo suficientemente pequeno após {iteracao+1} iterações")
            break

        iteracao += 1

    # Fase de Newton-Raphson
    x = (a + b) / 2
    print(f"\nIniciando Newton-Raphson com x0 = {x:.6f}")
    newton_iter = 0
    
    while newton_iter < MAX_ITER_TOTAL - iteracao:
        fx = funcao(x)
        dfx = derivada(x)
        
        if abs(dfx) < 1e-15:
            print("Derivada próxima de zero. Usando resultado atual.")
            return x

        x_new = x - fx / dfx
        fx_new = funcao(x_new)
        newton_iter += 1
        
        print(f"Iteração {iteracao + newton_iter}: x = {x_new:.16e}, f(x) = {fx_new:.16e}")

        if abs(fx_new) < TOL_NEWTON or abs(x_new - x) < TOL_NEWTON:
            print("Convergência alcançada.")
            x = x_new
            break

        x = x_new

    print(f"\nTotal de iterações: {iteracao + newton_iter}")
    return x

# Executar o método
print("\nIniciando cálculo da raiz...")
raiz = bissecao_newton_raphson(a, b)

if raiz is not None:
    print(f"\nRaiz aproximada: {raiz:.16e}")
    print(f"Valor da função na raiz: {funcao(raiz):.4e}")
else:
    print("\nNão foi possível encontrar uma raiz no intervalo fornecido.")
