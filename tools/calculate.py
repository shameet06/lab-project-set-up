import re


def calculate(expression):
    """Evaluate an arithmetic expression and return the result as a string.

    >>> calculate("2 + 3 * 4")
    '14'
    >>> calculate("(2 + 3) * 4")
    '20'
    >>> calculate("len('abc')")
    'Invalid expression'
    >>> calculate("2 ** 8")
    'Invalid expression'
    >>> calculate("4 / 0")
    'Invalid expression'
    >>> calculate("()")
    'Invalid expression'
    """
    expression = expression.strip()

    if not re.fullmatch(r'[0-9. +*/()-]+', expression):
        return "Invalid expression"

    if "**" in expression or "//" in expression:
        return "Invalid expression"

    try:
        result = eval(expression, {"__builtins__": {}})
    except (SyntaxError, ArithmeticError, TypeError, ValueError):
        return "Invalid expression"

    if not isinstance(result, (int, float)):
        return "Invalid expression"

    return str(result)
