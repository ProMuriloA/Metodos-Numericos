import sys
import math
import re
import numpy as np

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

def find_sign_change_intervals(f, min_val=-100, max_val=100, step=0.5):
    """Finds all intervals where the function changes sign or approaches zero"""
    print(f"\nSearching for intervals from {min_val} to {max_val}...")
    
    intervals = []
    x_prev = min_val
    f_prev = f(x_prev)
    
    # Also look for minima/maxima that might indicate roots for functions like x²
    critical_points = []
    
    x_current = x_prev + step
    while x_current <= max_val:
        f_current = f(x_current)
        
        # Skip if we get NaN values
        if math.isnan(f_prev) or math.isnan(f_current):
            x_prev = x_current
            f_prev = f_current
            x_current += step
            continue
        
        # Check for sign change
        if f_prev * f_current < 0:
            intervals.append((x_prev, x_current))
            print(f"Sign change found between {x_prev:.2f} and {x_current:.2f}")
        
        # Check for critical points (where derivative might be zero)
        if abs(f_current) < abs(f_prev) and abs(f_current) < 10:
            critical_points.append(x_current)
        
        x_prev = x_current
        f_prev = f_current
        x_current += step
    
    # If no sign changes found, check critical points
    if not intervals and critical_points:
        print("No sign changes found. Checking critical points...")
        for cp in critical_points:
            if abs(f(cp)) < 10:  # Arbitrary threshold
                intervals.append((cp - step, cp + step))
    
    return intervals

def numerical_derivative(f, x, h=1e-5):
    """Calculates numerical derivative using central differences"""
    return (f(x + h) - f(x - h)) / (2 * h)

def bisection_newton_hybrid(f, df, a, b, tol_bisection=1e-8, tol_newton=1e-15, max_iter=100):
    """Hybrid root-finding algorithm combining bisection and Newton-Raphson"""
    # Initial function evaluations
    fa, fb = f(a), f(b)
    
    # Check if we already have a root at endpoints
    if abs(fa) < tol_bisection:
        return a, 0, 'endpoint'
    if abs(fb) < tol_bisection:
        return b, 0, 'endpoint'
    
    # Verify sign change
    if fa * fb >= 0:
        # No sign change, check if we're dealing with a function like x²
        if abs(fa) < 10 and abs(fb) < 10:
            print("No sign change but function values are small. Trying Newton-Raphson from midpoint.")
            x0 = (a + b) / 2
            root, iters = newton_raphson(f, df, x0, tol_newton, max_iter)
            return root, iters, 'newton'
        else:
            print("No sign change and function values are not small. No root found in this interval.")
            return None, 0, 'no_root'
    
    iteration = 0
    
    # Bisection phase
    while iteration < max_iter:
        c = (a + b) / 2
        fc = f(c)
        
        if math.isnan(fc):
            print("NaN encountered during bisection. Aborting.")
            return None, iteration, 'error'
            
        print(f"Bisection iter {iteration+1}: a={a:.6f}, b={b:.6f}, c={c:.6f}, f(c)={fc:.6e}")
        
        # Check for convergence
        if abs(fc) < tol_bisection:
            print(f"Bisection converged after {iteration+1} iterations")
            return c, iteration, 'bisection'
            
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
    root, newton_iters = newton_raphson(f, df, x0, tol_newton, max_iter - iteration)
    
    return root, iteration + newton_iters, 'hybrid'

def newton_raphson(f, df, x0, tol=1e-15, max_iter=50):
    """Newton-Raphson method for root finding"""
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        
        # Check derivative
        if abs(dfx) < 1e-15:
            print(f"Small derivative ({dfx:.2e}) at iter {i+1}. Using current estimate.")
            return x, i+1
            
        # Newton step
        x_new = x - fx / dfx
        fx_new = f(x_new)
        
        print(f"Newton iter {i+1}: x={x_new:.16e}, f(x)={fx_new:.16e}")
        
        # Check convergence
        if abs(fx_new) < tol or abs(x_new - x) < tol:
            print(f"Newton converged after {i+1} iterations")
            return x_new, i+1
            
        x = x_new
    
    print(f"Newton-Raphson reached max iterations ({max_iter})")
    return x, max_iter

def find_all_roots(f, search_range=(-100, 100), step=0.5, tol=1e-10):
    """Finds all roots of a function within a given range"""
    # Create derivative function
    df = lambda x: numerical_derivative(f, x)
    
    # Find intervals with sign changes or critical points
    intervals = find_sign_change_intervals(f, search_range[0], search_range[1], step)
    
    if not intervals:
        print("No intervals found. Trying to find roots using Newton-Raphson at sample points.")
        # Sample function at various points and try Newton-Raphson
        sample_points = np.linspace(search_range[0], search_range[1], 20)
        intervals = [(x, x) for x in sample_points]
    
    roots = []
    iterations_per_root = []
    methods = []
    
    # Process each interval
    for i, (a, b) in enumerate(intervals):
        print(f"\nProcessing interval {i+1}: [{a:.2f}, {b:.2f}]")
        
        if a == b:
            # Single point - use as starting point for Newton-Raphson
            root, iters = newton_raphson(f, df, a)
            method = 'newton'
        else:
            # Interval - use hybrid method
            root, iters, method = bisection_newton_hybrid(f, df, a, b)
        
        if root is not None:
            # Check if this root is distinct from previous ones
            is_distinct = True
            for existing_root in roots:
                if abs(root - existing_root) < tol:
                    is_distinct = False
                    print(f"Root at {root:.8f} is similar to existing root {existing_root:.8f}")
                    break
            
            if is_distinct:
                # Verify it's actually a root
                fx = f(root)
                if abs(fx) < 1e-8:  # Strict tolerance for considering it a root
                    roots.append(root)
                    iterations_per_root.append(iters)
                    methods.append(method)
                    print(f"Found distinct root: {root:.16e} (in {iters} iterations)")
                else:
                    print(f"Rejecting candidate at {root:.8f} because f(x) = {fx:.4e} (not a root)")
            else:
                print(f"Skipping duplicate root: {root:.16e}")
        else:
            print(f"Failed to find root in interval [{a:.2f}, {b:.2f}]")
    
    return roots, iterations_per_root, methods

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
    
    # Find all roots
    roots, iterations, methods = find_all_roots(f)
    
    # Display results
    print("\n" + "="*70)
    print("ROOT FINDING RESULTS SUMMARY")
    print("="*70)
    
    if roots:
        # Sort roots
        roots_sorted = sorted(roots)
        
        for i, (root, iters, method) in enumerate(zip(roots_sorted, iterations, methods)):
            fx = f(root)
            print(f"Root {i+1}: x = {root:.16e}")
            print(f"         f(x) = {fx:.4e}")
            print(f"         Iterations: {iters}")
            print(f"         Method: {method}")
            print("-" * 50)
        
        print(f"\nTotal distinct roots found: {len(roots)}")
        
        # Check root validity
        valid_roots = [root for root in roots if abs(f(root)) < 1e-10]
        print(f"Valid roots (|f(x)| < 1e-10): {len(valid_roots)}")
    else:
        print("No roots found in the specified range.")
    
    print("="*70)

if __name__ == "__main__":
    main()
