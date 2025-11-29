"""Graph visualization module for Gaussian Graphical Models.

This module provides Manim scenes for visualizing Gaussian Graphical Models,
including their underlying graph structure and precision matrix.
"""

import networkx as nx
import numpy as np
from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    RED,
    RIGHT,
    UP,
    WHITE,
    Circle,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Scene,
    Text,
    VGroup,
    Write,
)


class GaussianGraphScene(Scene):
    """A Manim scene for visualizing a Gaussian Graphical Model.

    This scene demonstrates the relationship between a precision matrix
    (inverse covariance matrix) and the corresponding graph structure
    where edges represent conditional dependencies.
    """

    def construct(self):
        """Construct and animate the Gaussian Graphical Model visualization."""
        # Title
        title = Text("Gaussian Graphical Model", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create a sample precision matrix (4x4)
        # Non-zero off-diagonal entries indicate conditional dependence
        precision_matrix = np.array(
            [
                [1.0, 0.5, 0.0, 0.3],
                [0.5, 1.0, 0.4, 0.0],
                [0.0, 0.4, 1.0, 0.6],
                [0.3, 0.0, 0.6, 1.0],
            ]
        )

        # Create the graph from precision matrix
        graph = self._create_graph_from_precision(precision_matrix)
        graph_group = self._visualize_graph(graph)
        graph_group.shift(LEFT * 3)

        # Create the precision matrix display
        matrix_group = self._create_matrix_display(precision_matrix)
        matrix_group.shift(RIGHT * 3)

        # Animate both appearing
        self.play(FadeIn(graph_group), FadeIn(matrix_group))
        self.wait(1)

        # Add explanation
        explanation = Text(
            "Non-zero entries indicate edges\n(conditional dependencies)",
            font_size=24,
        )
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)

        # Clean up
        self.play(
            FadeOut(title),
            FadeOut(graph_group),
            FadeOut(matrix_group),
            FadeOut(explanation),
        )

    def _create_graph_from_precision(
        self, precision_matrix: np.ndarray, threshold: float = 1e-6
    ) -> nx.Graph:
        """Create a NetworkX graph from a precision matrix.

        Args:
            precision_matrix: The precision (inverse covariance) matrix.
            threshold: Threshold below which entries are considered zero.

        Returns:
            A NetworkX graph where edges represent non-zero off-diagonal entries.
        """
        n = precision_matrix.shape[0]
        graph = nx.Graph()
        graph.add_nodes_from(range(n))

        for i in range(n):
            for j in range(i + 1, n):
                if abs(precision_matrix[i, j]) > threshold:
                    graph.add_edge(i, j, weight=precision_matrix[i, j])

        return graph

    def _visualize_graph(self, graph: nx.Graph) -> VGroup:
        """Create a Manim visualization of a NetworkX graph.

        Args:
            graph: A NetworkX graph to visualize.

        Returns:
            A VGroup containing the graph visualization.
        """
        # Get node positions using a circular layout
        positions = nx.circular_layout(graph)

        # Scale positions for Manim
        scale = 2.0
        manim_positions = {
            node: np.array([pos[0] * scale, pos[1] * scale, 0])
            for node, pos in positions.items()
        }

        # Create nodes
        nodes = VGroup()
        node_labels = VGroup()
        for node in graph.nodes():
            circle = Circle(radius=0.3, color=BLUE, fill_opacity=0.5)
            circle.move_to(manim_positions[node])
            nodes.add(circle)

            label = MathTex(f"X_{{{node + 1}}}", font_size=24)
            label.move_to(manim_positions[node])
            node_labels.add(label)

        # Create edges
        edges = VGroup()
        for u, v in graph.edges():
            line = Line(manim_positions[u], manim_positions[v], color=WHITE)
            edges.add(line)

        return VGroup(edges, nodes, node_labels)

    def _create_matrix_display(self, matrix: np.ndarray) -> VGroup:
        """Create a visual representation of a matrix.

        Args:
            matrix: A numpy array to display.

        Returns:
            A VGroup containing the matrix visualization.
        """
        n = matrix.shape[0]
        matrix_group = VGroup()

        # Create matrix label
        label = MathTex(r"\Theta = ", font_size=36)
        label.shift(UP * 1.5)
        matrix_group.add(label)

        # Create matrix entries
        cell_size = 0.6
        entries = VGroup()
        for i in range(n):
            for j in range(n):
                value = matrix[i, j]
                if abs(value) < 1e-6:
                    text = MathTex("0", font_size=20)
                    text.set_color(RED)
                else:
                    text = MathTex(f"{value:.1f}", font_size=20)
                    if i == j:
                        text.set_color(GREEN)
                    else:
                        text.set_color(WHITE)

                x_pos = (j - (n - 1) / 2) * cell_size
                y_pos = ((n - 1) / 2 - i) * cell_size
                text.move_to([x_pos, y_pos, 0])
                entries.add(text)

        matrix_group.add(entries)
        return matrix_group


class GraphicalLassoScene(Scene):
    """A Manim scene demonstrating the Graphical Lasso algorithm.

    This scene shows how the Graphical Lasso sparsifies the precision
    matrix as the regularization parameter increases.
    """

    def construct(self):
        """Construct and animate the Graphical Lasso demonstration."""
        # Title
        title = Text("Graphical Lasso: Sparsity via Regularization", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Explanation of graphical lasso
        explanation = Text(
            "The Graphical Lasso estimates a sparse precision matrix\n"
            "by adding an L1 penalty to the likelihood.",
            font_size=24,
        )
        explanation.next_to(title, DOWN)
        self.play(Write(explanation))
        self.wait(1)

        # Show the optimization problem
        formula = MathTex(
            r"\hat{\Theta} = \arg\max_{\Theta \succ 0} "
            r"\left[ \log \det \Theta - \text{tr}(S\Theta) "
            r"- \lambda \|\Theta\|_1 \right]",
            font_size=32,
        )
        formula.next_to(explanation, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(2)

        # Clean up
        self.play(FadeOut(title), FadeOut(explanation), FadeOut(formula))


# Export scene for command-line rendering
__all__ = ["GaussianGraphScene", "GraphicalLassoScene"]
