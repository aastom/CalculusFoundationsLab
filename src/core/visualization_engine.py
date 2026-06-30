import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sympy

class VisualizationEngine:
    """
    Provides an API for creating interactive 2D and 3D visualizations
    of mathematical functions using Plotly.
    """

    def __init__(self):
        """Initializes the VisualizationEngine."""
        self.x, self.y = sympy.symbols('x y')

    def _evaluate_function(self, expr_str: str, x_vals: np.ndarray, y_vals: np.ndarray = None):
        """
        Evaluates a symbolic expression for given numpy array values.
        Handles both single-variable (y=f(x)) and multi-variable (z=f(x,y)) functions.

        Args:
            expr_str (str): The symbolic expression as a string.
            x_vals (np.ndarray): Array of x values.
            y_vals (np.ndarray, optional): Array of y values for 3D plots. Defaults to None.

        Returns:
            np.ndarray: Evaluated function values.

        Raises:
            ValueError: If the expression is invalid or evaluation fails.
        """
        try:
            expr = sympy.sympify(expr_str)
            if y_vals is None:
                # Single variable function f(x)
                f_np = sympy.lambdify(self.x, expr, 'numpy')
                return f_np(x_vals)
            else:
                # Multi-variable function f(x,y)
                X, Y = np.meshgrid(x_vals, y_vals)
                f_np = sympy.lambdify((self.x, self.y), expr, 'numpy')
                return f_np(X, Y)
        except (sympy.SympifyError, TypeError, Exception) as e:
            raise ValueError(f"Error evaluating function '{expr_str}': {e}")

    def plot_2d_function(self, expr_str: str, x_range=(-5, 5), num_points=200, title="2D Function Plot"):
        """
        Generates an interactive 2D plot of a single-variable function.

        Args:
            expr_str (str): The function expression (e.g., "x**2", "sin(x)").
            x_range (tuple): (min_x, max_x) for the x-axis.
            num_points (int): Number of points to sample for the plot.
            title (str): Title of the plot.

        Returns:
            go.Figure: A Plotly Figure object.
        """
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = self._evaluate_function(expr_str, x_vals)

        fig = go.Figure(
            data=[go.Scatter(x=x_vals, y=y_vals, mode='lines', name=expr_str)],
            layout=go.Layout(
                title=go.layout.Title(text=title),
                xaxis_title="x",
                yaxis_title="f(x)"
            )
        )
        return fig

    def plot_3d_surface(self, expr_str: str, x_range=(-5, 5), y_range=(-5, 5), num_points=50, title="3D Surface Plot"):
        """
        Generates an interactive 3D surface plot of a two-variable function.

        Args:
            expr_str (str): The function expression (e.g., "x**2 + y**2", "sin(x*y)").
            x_range (tuple): (min_x, max_x) for the x-axis.
            y_range (tuple): (min_y, max_y) for the y-axis.
            num_points (int): Number of points to sample for each axis.
            title (str): Title of the plot.

        Returns:
            go.Figure: A Plotly Figure object.
        """
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = np.linspace(y_range[0], y_range[1], num_points)
        z_vals = self._evaluate_function(expr_str, x_vals, y_vals)

        fig = go.Figure(
            data=[go.Surface(z=z_vals, x=x_vals, y=y_vals)],
            layout=go.Layout(
                title=go.layout.Title(text=title),
                scene=dict(
                    xaxis_title='x',
                    yaxis_title='y',
                    zaxis_title='f(x,y)'
                )
            )
        )
        return fig

    def plot_riemann_sum(self, expr_str: str, x_range=(0, 5), num_rectangles=10, method='right', title="Riemann Sum Visualization"):
        """
        Generates a 2D plot visualizing a Riemann sum for a function.

        Args:
            expr_str (str): The function expression.
            x_range (tuple): (min_x, max_x) for the x-axis.
            num_rectangles (int): Number of rectangles for the approximation.
            method (str): 'left', 'right', or 'midpoint' for rectangle height.
            title (str): Title of the plot.

        Returns:
            go.Figure: A Plotly Figure object.
        """
        a, b = x_range
        x_vals_full = np.linspace(a, b, 500) # For smooth function curve
        y_vals_full = self._evaluate_function(expr_str, x_vals_full)

        # Rectangle data
        dx = (b - a) / num_rectangles
        x_rect = np.linspace(a, b - dx, num_rectangles) # Left edges
        if method == 'right':
            sample_points = x_rect + dx
        elif method == 'midpoint':
            sample_points = x_rect + dx / 2
        else: # 'left'
            sample_points = x_rect

        y_rect_heights = self._evaluate_function(expr_str, sample_points)

        rect_x_coords = []
        rect_y_coords = []
        for i in range(num_rectangles):
            rect_x_coords.extend([x_rect[i], x_rect[i], x_rect[i] + dx, x_rect[i] + dx, x_rect[i]])
            rect_y_coords.extend([0, y_rect_heights[i], y_rect_heights[i], 0, 0])
            rect_x_coords.append(None) # Separate rectangles
            rect_y_coords.append(None)

        fig = go.Figure(
            data=[
                go.Scatter(x=x_vals_full, y=y_vals_full, mode='lines', name=expr_str, line=dict(color='blue')),
                go.Scatter(
                    x=rect_x_coords, y=rect_y_coords, mode='lines', fill='toself',
                    fillcolor='rgba(255,0,0,0.4)', line=dict(color='red', width=1), name='Riemann Rectangles'
                )
            ],
            layout=go.Layout(
                title=go.layout.Title(text=title),
                xaxis_title="x",
                yaxis_title="f(x)",
                showlegend=True
            )
        )
        return fig

# Example usage (for demonstration/testing purposes)
if __name__ == "__main__":
    viz_engine = VisualizationEngine()

    # 2D Plot
    fig2d = viz_engine.plot_2d_function("x**2", x_range=(-3, 3), title="Parabola: f(x) = x^2")
    # fig2d.show() # Uncomment to display plot if running locally
    print("Generated 2D plot for x^2")

    # 3D Plot
    fig3d = viz_engine.plot_3d_surface("x**2 + y**2", x_range=(-2, 2), y_range=(-2, 2), title="Paraboloid: f(x,y) = x^2 + y^2")
    # fig3d.show() # Uncomment to display plot if running locally
    print("Generated 3D plot for x^2 + y^2")

    # Riemann Sum Plot
    fig_riemann = viz_engine.plot_riemann_sum("sin(x) + 2", x_range=(0, 2 * np.pi), num_rectangles=20, method='right', title="Riemann Sum for sin(x) + 2")
    # fig_riemann.show() # Uncomment to display plot if running locally
    print("Generated Riemann Sum plot for sin(x) + 2")

    try:
        viz_engine.plot_2d_function("invalid_func(x)")
    except ValueError as e:
        print(f"Error handling invalid function for 2D plot: {e}")
