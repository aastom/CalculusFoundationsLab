import sympy

class SymbolicEngine:
    """
    Provides a wrapper for SymPy operations to perform symbolic calculus.
    This class centralizes symbolic computations, ensuring consistency
    and simplifying interactions with the underlying SymPy library.
    """

    def __init__(self):
        """Initializes the SymbolicEngine."""
        self.x, self.y, self.z, self.t = sympy.symbols('x y z t')
        self.f, self.g, self.h = sympy.symbols('f g h', cls=sympy.Function)

    def parse_expression(self, expr_str: str):
        """
        Parses a string into a SymPy expression.

        Args:
            expr_str: The string representation of the mathematical expression.

        Returns:
            A SymPy expression object.
        """
        try:
            return sympy.sympify(expr_str, locals={'x': self.x, 'y': self.y, 't': self.t})
        except (sympy.SympifyError, TypeError) as e:
            raise ValueError(f"Invalid expression: {expr_str}. Error: {e}")

    def diff_expr(self, expr_str: str, var_str: str = 'x'):
        """
        Differentiates a given expression with respect to a specified variable.

        Args:
            expr_str: The expression to differentiate (as a string).
            var_str: The variable to differentiate with respect to (default 'x').

        Returns:
            A string representation of the derivative.
        """
        expr = self.parse_expression(expr_str)
        var = sympy.symbols(var_str)
        derivative = sympy.diff(expr, var)
        return str(derivative)

    def integrate_expr(self, expr_str: str, var_str: str = 'x', definite_limits=None):
        """
        Integrates a given expression with respect to a specified variable.

        Args:
            expr_str: The expression to integrate (as a string).
            var_str: The variable to integrate with respect to (default 'x').
            definite_limits: A tuple (lower_limit, upper_limit) for definite integrals.

        Returns:
            A string representation of the integral.
        """
        expr = self.parse_expression(expr_str)
        var = sympy.symbols(var_str)
        if definite_limits:
            lower, upper = definite_limits
            integral = sympy.integrate(expr, (var, lower, upper))
        else:
            integral = sympy.integrate(expr, var)
        return str(integral)

    def limit_expr(self, expr_str: str, var_str: str, point, dir='+-'):
        """
        Calculates the limit of an expression as a variable approaches a point.

        Args:
            expr_str: The expression (as a string).
            var_str: The variable approaching the point.
            point: The point the variable approaches.
            dir: The direction of approach ('+' for from above, '-' for from below, '+-' for both).

        Returns:
            A string representation of the limit.
        """
        expr = self.parse_expression(expr_str)
        var = sympy.symbols(var_str)
        limit_val = sympy.limit(expr, var, point, dir=dir)
        return str(limit_val)

    def simplify_expr(self, expr_str: str):
        """
        Simplifies a given expression.

        Args:
            expr_str: The expression to simplify (as a string).

        Returns:
            A string representation of the simplified expression.
        """
        expr = self.parse_expression(expr_str)
        simplified = sympy.simplify(expr)
        return str(simplified)

# Example usage (for demonstration/testing purposes)
if __name__ == "__main__":
    engine = SymbolicEngine()

    # Differentiate
    deriv1 = engine.diff_expr("x**2 + sin(x)")
    print(f"Derivative of x^2 + sin(x): {deriv1}") # Expected: 2*x + cos(x)

    deriv2 = engine.diff_expr("exp(y) * y", var_str='y')
    print(f"Derivative of e^y * y with respect to y: {deriv2}") # Expected: y*exp(y) + exp(y)

    # Integrate
    integ1 = engine.integrate_expr("2*x + cos(x)")
    print(f"Integral of 2x + cos(x): {integ1}") # Expected: x**2 + sin(x)

    integ2 = engine.integrate_expr("x**2", definite_limits=(0, 1))
    print(f"Definite integral of x^2 from 0 to 1: {integ2}") # Expected: 1/3

    # Limit
    limit1 = engine.limit_expr("sin(x)/x", 'x', 0)
    print(f"Limit of sin(x)/x as x->0: {limit1}") # Expected: 1

    limit2 = engine.limit_expr("1/x", 'x', 0, dir='+')
    print(f"Limit of 1/x as x->0+ : {limit2}") # Expected: oo (infinity)

    # Simplify
    simp1 = engine.simplify_expr("sin(x)**2 + cos(x)**2")
    print(f"Simplify sin(x)^2 + cos(x)^2: {simp1}") # Expected: 1

    try:
        engine.parse_expression("invalid_function(x)")
    except ValueError as e:
        print(f"Error handling invalid expression: {e}")
