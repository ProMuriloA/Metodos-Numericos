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

def encontrar_intervalos(f, inicio=-10, fim=10, passo=0.5):
    """Encontra todos os intervalos com troca de sinal dentro de um range"""
    print("Procurando intervalos com troca de sinal...")
    intervalos = []
    x_atual = inicio
    f_anterior = f(x_atual)
    
    while x_atual <= fim:
        x_proximo = x_atual + passo
        if x_proximo > fim:
            break
        f_atual = f(x_proximo)
        
        if math.isnan(f_anterior) or math.isnan(f_atual):
            x_atual = x_proximo
            f_anterior = f_atual
            continue
        
        if f_anterior * f_atual < 0:
            intervalo = (x_atual, x_proximo)
            intervalos.append(intervalo)
            print(f"Troca de sinal encontrada entre {x_atual:.2f} e {x_proximo:.2f}")
        
        x_atual = x_proximo
        f_anterior = f_atual
    
    return intervalos

# Solicitar a função do usuário
funcao_str = input("\nDigite a função f(x) (use 'x' como variável, ex: x**2 - 2): ")

# Converter notações de potência
funcao_str_convertida = converter_potencia(funcao_str)
print(f"Expressão convertida: {funcao_str_convertida}")

# Criar função matemática
funcao = string_para_funcao(funcao_str_convertida)

# Encontrar todos os intervalos com troca de sinal
intervalos = encontrar_intervalos(funcao)

if not intervalos:
    print("Nenhum intervalo com troca de sinal encontrado. Insira manualmente.")
    a = float(input("Digite o valor inicial do intervalo (a): "))
    b = float(input("Digite o valor final do intervalo (b): "))
    intervalos = [(a, b)]

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

# Encontrar e exibir todas as raízes
raizes = []
tolerancia_raiz = 1e-5

for a, b in intervalos:
    print(f"\nCalculando raiz no intervalo [{a}, {b}]")
    raiz = bissecao_newton_raphson(a, b)
    
    if raiz is not None:
        # Verificar se a raiz já foi encontrada
        if not any(abs(raiz - r) < tolerancia_raiz for r in raizes):
            raizes.append(raiz)
            print(f"Raiz encontrada: {raiz:.16e}")
        else:
            print(f"Raiz duplicada ignorada: {raiz:.16e}")
    else:
        print("Não foi possível encontrar uma raiz neste intervalo.")

# Exibir resumo completo de todas as raízes encontradas
print("\n" + "="*60)
print("RESUMO DAS RAÍZES ENCONTRADAS")
print("="*60)

if raizes:
    raizes_ordenadas = sorted(raizes)
    for i, raiz in enumerate(raizes_ordenadas, 1):
        valor_funcao = funcao(raiz)
        print(f"Raiz {i}: x = {raiz:.16e}")
        print(f"         f(x) = {valor_funcao:.4e}")
        print(f"         Intervalo inicial: [{next((a for a, b in intervalos if min(a, b) <= raiz <= max(a, b)), 'N/A'):.2f}, " +
              f"{next((b for a, b in intervalos if min(a, b) <= raiz <= max(a, b)), 'N/A'):.2f}]")
        print("-" * 40)
    
    print(f"\nTotal de raízes distintas encontradas: {len(raizes)}")
    
    # Verificar se todas as raízes são válidas (f(x) próximo de zero)
    raizes_validas = [raiz for raiz in raizes if abs(funcao(raiz)) < 1e-10]
    print(f"Raízes válidas (|f(x)| < 1e-10): {len(raizes_validas)}")
    
else:
    print("Nenhuma raiz encontrada nos intervalos fornecidos.")

print("="*60)
