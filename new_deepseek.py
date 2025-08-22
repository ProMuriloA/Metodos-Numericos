import sys
import math
import re

def convert_power_notation(expr_str):
    """Converts all power notations to Python syntax (base**exponent)"""
    # Unicode exponents
    unicode_subs = {
        '²': '**2', '³': '**3', '⁴': '**4', '⁵': '**5', 
        '⁶': '**6', '⁷': '**7', '⁸': '**8', '⁹': '**9', '⁰': '**0'
    }
    for char, repl in unicode_subs.items():
        expr_str = expr_str.replace(char, repl)
    
    # Circumflex notation
    expr_str = re.sub(r'(\d*\.?\d+|\b\w+|[\)])\s*\^\s*(\d*\.?\d+|\b\w+|[\()])', r'\1**\2', expr_str)
    
    # Implicit multiplication
    expr_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr_str)
    expr_str = re.sub(r'([a-zA-Z\)])(\d)', r'\1*\2', expr_str)
    
    return expr_str

def string_to_function(expr: str):
    """Converts a math expression string to an executable Python function"""
    env = {
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
        local_env = {**env, 'x': x}
        try:
            return eval(expr, {'__builtins__': None}, local_env)
        except Exception as e:
            print(f"Error evaluating function at x={x}: {e}")
            return float('nan')
    
    return f

def find_sign_change_interval(f, min_val=-100, max_val=100, step=1.0):
    """Automatically finds an interval where the function changes sign"""
    print("\nSearching for sign change interval...")
    
    # Create evaluation points from min_val to max_val
    x_vals = [min_val + i*step for i in range(int((max_val - min_val)/step) + 1)]
    
    valid_points = []
    for x in x_vals:
        try:
            fx = f(x)
            if not math.isnan(fx):
                print(f"f({x:7.2f}) = {fx:12.6e}")
                valid_points.append((x, fx))
        except:
            continue
    
    # Check for sign changes between consecutive points
    for i in range(len(valid_points) - 1):
        x1, f1 = valid_points[i]
        x2, f2 = valid_points[i+1]
        
        if f1 * f2 < 0:
            print(f"\nSign change found between {x1:.2f} and {x2:.2f}")
            print(f"f({x1:.2f}) = {f1:.6e}")
            print(f"f({x2:.2f}) = {f2:.6e}")
            return min(x1, x2), max(x1, x2)
        elif f1 == 0:
            print(f"\nExact root found at x = {x1:.6f}")
            return x1, x1
        elif f2 == 0:
            print(f"\nExact root found at x = {x2:.6f}")
            return x2, x2
    
    return None

def numerical_derivative(f, x, h=1e-5):
    """Calculates numerical derivative using central differences"""
    return (f(x + h) - f(x - h)) / (2 * h)

def bisection_newton_hybrid(f, df, a, b, tol_bisection=1e-8, tol_newton=1e-15, max_iter=100):
    """Hybrid root-finding algorithm combining bisection and Newton-Raphson"""
    # Initial function evaluations
    fa, fb = f(a), f(b)
    
    # Check if we already have a root at endpoints
    if fa == 0:
        return a
    if fb == 0:
        return b
    
    # Verify sign change
    if fa * fb >= 0:
        print("No sign change in initial interval. Using Newton-Raphson directly.")
        # Start from midpoint
        x0 = (a + b) / 2
        return newton_raphson(f, df, x0, tol_newton, max_iter)
    
    iteration = 0
    
    # Bisection phase
    while iteration < max_iter:
        c = (a + b) / 2
        fc = f(c)
        
        if math.isnan(fc):
            print("NaN encountered during bisection. Aborting.")
            return None
            
        print(f"Bisection iter {iteration+1}: a={a:.6f}, b={b:.6f}, c={c:.6f}, f(c)={fc:.6e}")
        
        # Check for convergence
        if abs(fc) < tol_bisection:
            print(f"Bisection converged after {iteration+1} iterations")
            return c
            
        # Update interval
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
            
        # Check interval size
        if abs(b - a) < tol_bisection:
            print(f"Small interval after {iteration+1} bisection iterations")
            break
            
        iteration += 1
    
    # Newton-Raphson phase starting from bisection result
    x0 = (a + b) / 2
    print(f"\nStarting Newton-Raphson from x0 = {x0:.6f}")
    return newton_raphson(f, df, x0, tol_newton, max_iter - iteration)

def newton_raphson(f, df, x0, tol=1e-15, max_iter=50):
    """Newton-Raphson method for root finding"""
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        
        # Check derivative
        if abs(dfx) < 1e-15:
            print(f"Small derivative ({dfx:.2e}) at iter {i+1}. Using current estimate.")
            return x
            
        # Newton step
        x_new = x - fx / dfx
        fx_new = f(x_new)
        
        print(f"Newton iter {i+1}: x={x_new:.16e}, f(x)={fx_new:.16e}")
        
        # Check convergence
        if abs(fx_new) < tol or abs(x_new - x) < tol:
            print(f"Newton converged after {i+1} iterations")
            return x_new
            
        x = x_new
    
    print(f"Newton-Raphson reached max iterations ({max_iter})")
    return x

def main():
    """Main program execution"""
    # Get function from user
    function_str = input("\nEnter the function f(x) (use 'x' as variable, e.g., x**2 - 2): ")
    
    # Convert power notation
    converted_str = convert_power_notation(function_str)
    print(f"Converted expression: {converted_str}")
    
    # Create executable function
    f = string_to_function(converted_str)
    
    # Test function at x=0
    try:
        test_val = f(0)
        print(f"Test f(0) = {test_val:.6e}")
    except:
        print("Function test failed. Please check your expression.")
        return
    
    # Find sign change interval automatically from -100 to 100
    interval = find_sign_change_interval(f, min_val=-100, max_val=100)
    
    if interval is None:
        print("Could not find sign change automatically. Please enter interval manually.")
        a = float(input("Enter start of interval (a): "))
        b = float(input("Enter end of interval (b): "))
    elif interval[0] == interval[1]:
        # We found an exact root during search
        root = interval[0]
        print(f"\nRoot found during search: {root:.16e}")
        print(f"f(root) = {f(root):.4e}")
        return
    else:
        a, b = interval
    
    # Create derivative function
    df = lambda x: numerical_derivative(f, x)
    
    # Find root
    print("\nStarting hybrid root-finding algorithm...")
    root = bisection_newton_hybrid(f, df, a, b)
    
    if root is not None:
        print(f"\nApproximate root: {root:.16e}")
        print(f"Function value at root: {f(root):.4e}")
    else:
        print("\nRoot finding failed.")

if __name__ == "__main__":
    main()