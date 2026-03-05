"""
Mathematical Foundation Services
Modular arithmetic, Euclidean algorithms, fast exponentiation.
"""


def modular_arithmetic(a: int, b: int, mod: int, operation: str = "add") -> dict:
    """Visualize modular arithmetic operations."""
    steps = []
    if operation == "add":
        raw = a + b
        result = raw % mod
        steps.append({"formula": f"{a} + {b} = {raw}", "operation": "addition"})
        steps.append({"formula": f"{raw} mod {mod} = {result}", "operation": "modulo"})
        math_expr = f"({a} + {b}) mod {mod} = {result}"
    elif operation == "subtract":
        raw = a - b
        result = raw % mod
        steps.append({"formula": f"{a} - {b} = {raw}", "operation": "subtraction"})
        steps.append({"formula": f"{raw} mod {mod} = {result}", "operation": "modulo"})
        math_expr = f"({a} - {b}) mod {mod} = {result}"
    elif operation == "multiply":
        raw = a * b
        result = raw % mod
        steps.append({"formula": f"{a} × {b} = {raw}", "operation": "multiplication"})
        steps.append({"formula": f"{raw} mod {mod} = {result}", "operation": "modulo"})
        math_expr = f"({a} × {b}) mod {mod} = {result}"
    elif operation == "power":
        raw = a ** b
        result = pow(a, b, mod)
        steps.append({"formula": f"{a}^{b} = {raw}", "operation": "exponentiation"})
        steps.append({"formula": f"{raw} mod {mod} = {result}", "operation": "modulo"})
        math_expr = f"{a}^{b} mod {mod} = {result}"
    else:
        return {"error": f"Unknown operation: {operation}"}

    return {
        "a": a, "b": b, "mod": mod,
        "operation": operation,
        "result": result,
        "steps": steps,
        "math": math_expr
    }


def euclidean_algorithm(a: int, b: int) -> dict:
    """Step-by-step Euclidean Algorithm to find GCD."""
    if a < 0:
        a = -a
    if b < 0:
        b = -b

    original_a, original_b = a, b
    steps = []
    iteration = 0

    while b != 0:
        q = a // b
        r = a % b
        steps.append({
            "iteration": iteration,
            "a": a, "b": b,
            "quotient": q, "remainder": r,
            "formula": f"{a} = {q} × {b} + {r}"
        })
        a, b = b, r
        iteration += 1

    return {
        "input": {"a": original_a, "b": original_b},
        "gcd": a,
        "steps": steps,
        "total_iterations": iteration,
        "math": f"gcd({original_a}, {original_b}) = {a}"
    }


def extended_euclidean(a: int, b: int) -> dict:
    """Extended Euclidean Algorithm: find gcd, x, y such that ax + by = gcd."""
    original_a, original_b = a, b

    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    steps = []
    iteration = 0

    while r != 0:
        q = old_r // r
        steps.append({
            "iteration": iteration,
            "quotient": q,
            "r": old_r, "s": old_s, "t": old_t,
            "formula": f"q = {old_r} ÷ {r} = {q}"
        })
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
        iteration += 1

    # Final row
    steps.append({
        "iteration": iteration,
        "r": old_r, "s": old_s, "t": old_t,
        "formula": "final"
    })

    return {
        "input": {"a": original_a, "b": original_b},
        "gcd": old_r, "x": old_s, "y": old_t,
        "steps": steps,
        "verification": f"{original_a}×{old_s} + {original_b}×{old_t} = {original_a * old_s + original_b * old_t}",
        "math": f"{original_a}·({old_s}) + {original_b}·({old_t}) = {old_r}"
    }


def modular_inverse(a: int, m: int) -> dict:
    """Find modular inverse using Extended Euclidean Algorithm."""
    g, x, y = _ext_gcd(a % m, m)
    if g != 1:
        return {
            "input": {"a": a, "m": m},
            "exists": False,
            "reason": f"gcd({a}, {m}) = {g} ≠ 1, so inverse does not exist.",
            "math": f"{a}⁻¹ mod {m} = DNE"
        }
    inv = x % m
    eea = extended_euclidean(a % m, m)
    return {
        "input": {"a": a, "m": m},
        "exists": True,
        "inverse": inv,
        "verification": f"{a} × {inv} mod {m} = {(a * inv) % m}",
        "extended_euclidean_steps": eea["steps"],
        "math": f"{a}⁻¹ mod {m} = {inv}"
    }


def _ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = _ext_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


def fast_exponentiation(base: int, exp: int, mod: int) -> dict:
    """Square-and-multiply algorithm with step visualization."""
    binary = bin(exp)[2:]
    steps = []
    result = 1

    for i, bit in enumerate(binary):
        old_result = result
        result = (result * result) % mod
        steps.append({
            "step": i,
            "bit": bit,
            "operation": f"Square: {old_result}² mod {mod} = {result}",
            "result_after_square": result
        })
        if bit == '1':
            old_result2 = result
            result = (result * base) % mod
            steps[-1]["operation"] += f" → Multiply: {old_result2} × {base} mod {mod} = {result}"
            steps[-1]["result_after_multiply"] = result
        steps[-1]["current_result"] = result

    return {
        "base": base, "exponent": exp, "mod": mod,
        "binary_exponent": binary,
        "result": result,
        "steps": steps,
        "math": f"{base}^{exp} mod {mod} = {result}"
    }
