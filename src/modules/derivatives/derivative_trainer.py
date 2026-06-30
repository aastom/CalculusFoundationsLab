import random
from sympy import symbols, diff, sympify
from src.core.symbolic_engine import SymbolicEngine # Assuming src is in PYTHONPATH or relative import works

class DerivativeTrainer:
    """
    A module for practicing and testing derivative calculation skills.
    It generates various derivative problems and checks user answers
    using the symbolic engine.
    """

    def __init__(self, symbolic_engine: SymbolicEngine):
        """
        Initializes the DerivativeTrainer with a SymbolicEngine instance.

        Args:
            symbolic_engine: An instance of SymbolicEngine for calculus operations.
        """
        self.engine = symbolic_engine
        self.x = symbols('x')
        self.problem_types = [
            "power", "product", "quotient", "chain",
            "trigonometric", "exponential", "logarithmic"
        ]

    def _generate_power_rule_problem(self):
        base_expr = f"x**{random.randint(2, 5)}"
        coeff = random.randint(1, 4)
        problem_expr = f"{coeff}*{base_expr}"
        return problem_expr

    def _generate_product_rule_problem(self):
        f_x = random.choice([f"x**{random.randint(1, 3)}", "sin(x)", "exp(x)"])
        g_x = random.choice([f"x**{random.randint(1, 3)}", "cos(x)", "log(x)"])
        problem_expr = f"({f_x}) * ({g_x})"
        return problem_expr

    def _generate_quotient_rule_problem(self):
        num = random.choice([f"x**{random.randint(2, 4)}", "exp(x)"])
        den = random.choice([f"x**{random.randint(1, 2)}", "cos(x)"])
        problem_expr = f"({num}) / ({den})"
        return problem_expr

    def _generate_chain_rule_problem(self):
        outer = random.choice([f"u**{random.randint(2, 4)}", "sin(u)", "exp(u)"])
        inner = random.choice([f"x**{random.randint(1, 2)} + {random.randint(1, 3)}", "cos(x)"])
        problem_expr = outer.replace("u", f"({inner})")
        return problem_expr

    def _generate_trig_problem(self):
        func = random.choice(["sin(x)", "cos(x)", "tan(x)"])
        coeff = random.randint(1, 3)
        power = random.randint(1,2)
        problem_expr = f"{coeff}*({func})**{power}"
        return problem_expr

    def _generate_exp_log_problem(self):
        type = random.choice(["exp", "log"])
        if type == "exp":
            problem_expr = f"exp({random.randint(1, 3)}*x)"
        else:
            problem_expr = f"log({random.randint(1, 3)}*x)"
        return problem_expr

    def generate_problem(self, problem_type: str = None):
        """
        Generates a random derivative problem.

        Args:
            problem_type (str, optional): Specific type of problem to generate
                                         (e.g., "power", "product"). If None, a random type is chosen.

        Returns:
            tuple: (problem_expression_string, correct_answer_string)
        """
        if problem_type and problem_type not in self.problem_types:
            raise ValueError(f"Invalid problem type: {problem_type}. Choose from {self.problem_types}")

        selected_type = problem_type if problem_type else random.choice(self.problem_types)

        if selected_type == "power":
            problem_expr = self._generate_power_rule_problem()
        elif selected_type == "product":
            problem_expr = self._generate_product_rule_problem()
        elif selected_type == "quotient":
            problem_expr = self._generate_quotient_rule_problem()
        elif selected_type == "chain":
            problem_expr = self._generate_chain_rule_problem()
        elif selected_type == "trigonometric":
            problem_expr = self._generate_trig_problem()
        elif selected_type == "exponential" or selected_type == "logarithmic":
            problem_expr = self._generate_exp_log_problem()
        else:
            problem_expr = "x**2" # Fallback

        correct_deriv = self.engine.diff_expr(problem_expr, 'x')
        return problem_expr, correct_deriv

    def check_answer(self, problem_expr: str, user_answer_str: str):
        """
        Checks if the user's answer for a derivative problem is correct.

        Args:
            problem_expr (str): The original expression for which the derivative was taken.
            user_answer_str (str): The user's submitted answer for the derivative.

        Returns:
            bool: True if the answer is symbolically equivalent to the correct derivative, False otherwise.
            str: Feedback message.
        """
        try:
            correct_deriv_sym = sympify(self.engine.diff_expr(problem_expr, 'x'))
            user_answer_sym = sympify(user_answer_str)

            # Check for symbolic equivalence after simplification
            if sympy.simplify(correct_deriv_sym - user_answer_sym) == 0:
                return True, "Correct!"
            else:
                return False, f"Incorrect. The correct answer is: {correct_deriv_sym}"
        except (sympy.SympifyError, ValueError) as e:
            return False, f"Could not parse your answer or the problem expression. Error: {e}"

# Example usage (for demonstration/testing purposes)
if __name__ == "__main__":
    sym_engine = SymbolicEngine()
    trainer = DerivativeTrainer(sym_engine)

    print("--- Derivative Trainer Examples ---")

    # Generate a random problem
    prob_expr, correct_ans = trainer.generate_problem()
    print(f"Problem: Find the derivative of f(x) = {prob_expr}")
    print(f"Correct Answer (for verification): {correct_ans}")

    # Simulate a user attempt (correct)
    user_attempt_correct = sym_engine.diff_expr(prob_expr) # User correctly calculates it
    is_correct, feedback = trainer.check_answer(prob_expr, user_attempt_correct)
    print(f"User's attempt: {user_attempt_correct}")
    print(f"Result: {is_correct}, Feedback: {feedback}\n")

    # Simulate a user attempt (incorrect)
    prob_expr_inc, correct_ans_inc = trainer.generate_problem(problem_type="power")
    print(f"Problem: Find the derivative of f(x) = {prob_expr_inc}")
    print(f"Correct Answer (for verification): {correct_ans_inc}")
    user_attempt_incorrect = "0" # Clearly wrong
    is_correct, feedback = trainer.check_answer(prob_expr_inc, user_attempt_incorrect)
    print(f"User's attempt: {user_attempt_incorrect}")
    print(f"Result: {is_correct}, Feedback: {feedback}\n")

    # Generate a chain rule problem
    prob_expr_chain, correct_ans_chain = trainer.generate_problem(problem_type="chain")
    print(f"Problem (Chain Rule): Find the derivative of f(x) = {prob_expr_chain}")
    print(f"Correct Answer (for verification): {correct_ans_chain}")
    user_attempt_chain = sym_engine.diff_expr(prob_expr_chain) # User correctly calculates it
    is_correct, feedback = trainer.check_answer(prob_expr_chain, user_attempt_chain)
    print(f"User's attempt: {user_attempt_chain}")
    print(f"Result: {is_correct}, Feedback: {feedback}\n")

    # Example with invalid user input
    prob_expr_invalid, _ = trainer.generate_problem(problem_type="trigonometric")
    print(f"Problem: Find the derivative of f(x) = {prob_expr_invalid}")
    is_correct, feedback = trainer.check_answer(prob_expr_invalid, "garbage")
    print(f"User's attempt: garbage")
    print(f"Result: {is_correct}, Feedback: {feedback}\n")
