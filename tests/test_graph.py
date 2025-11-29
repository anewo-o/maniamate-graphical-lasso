"""Tests for the graph module."""

import numpy as np

from ggm_viz.graph import GaussianGraphScene


class TestGaussianGraphScene:
    """Tests for the GaussianGraphScene class."""

    def test_create_graph_from_precision(self):
        """Test that a graph is correctly created from a precision matrix."""
        scene = GaussianGraphScene()

        # Create a simple precision matrix
        precision_matrix = np.array(
            [
                [1.0, 0.5, 0.0],
                [0.5, 1.0, 0.3],
                [0.0, 0.3, 1.0],
            ]
        )

        graph = scene._create_graph_from_precision(precision_matrix)

        # Check that the graph has the correct number of nodes
        assert graph.number_of_nodes() == 3

        # Check that the graph has the correct edges (0-1 and 1-2)
        assert graph.has_edge(0, 1)
        assert graph.has_edge(1, 2)
        assert not graph.has_edge(0, 2)

    def test_create_graph_from_precision_with_threshold(self):
        """Test that small values are correctly thresholded."""
        scene = GaussianGraphScene()

        # Create a precision matrix with a small value
        precision_matrix = np.array(
            [
                [1.0, 0.5, 1e-8],
                [0.5, 1.0, 0.3],
                [1e-8, 0.3, 1.0],
            ]
        )

        graph = scene._create_graph_from_precision(precision_matrix, threshold=1e-6)

        # The small value should be treated as zero
        assert not graph.has_edge(0, 2)

    def test_create_graph_empty_precision(self):
        """Test that a diagonal matrix produces a graph with no edges."""
        scene = GaussianGraphScene()

        # Diagonal matrix (no off-diagonal entries)
        precision_matrix = np.eye(4)

        graph = scene._create_graph_from_precision(precision_matrix)

        assert graph.number_of_nodes() == 4
        assert graph.number_of_edges() == 0

    def test_create_graph_fully_connected(self):
        """Test that a full matrix produces a fully connected graph."""
        scene = GaussianGraphScene()

        # Full matrix (all entries non-zero)
        precision_matrix = np.array(
            [
                [1.0, 0.5, 0.3],
                [0.5, 1.0, 0.4],
                [0.3, 0.4, 1.0],
            ]
        )

        graph = scene._create_graph_from_precision(precision_matrix)

        assert graph.number_of_nodes() == 3
        # For 3 nodes fully connected: 3 edges
        assert graph.number_of_edges() == 3
