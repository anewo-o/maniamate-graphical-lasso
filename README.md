# maniamate-graphical-lasso

A Python Manim project for visualizing Gaussian Graphical Models and the Graphical Lasso algorithm.

## Overview

This project provides animated visualizations of:
- **Gaussian Graphical Models (GGM)**: Visual representation of the relationship between precision matrices and graph structures
- **Graphical Lasso**: Demonstration of how L1 regularization induces sparsity in precision matrix estimation

## Installation

### Prerequisites

Make sure you have Python 3.9+ installed. Manim also requires some system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg

# macOS
brew install cairo pango ffmpeg
```

### Install the package

```bash
# Clone the repository
git clone https://github.com/anewo-o/maniamate-graphical-lasso.git
cd maniamate-graphical-lasso

# Install in development mode
pip install -e ".[dev]"
```

## Usage

### Render a visualization

```bash
# Render the Gaussian Graphical Model scene
manim -pql src/ggm_viz/graph.py GaussianGraphScene

# Render the Graphical Lasso explanation scene
manim -pql src/ggm_viz/graph.py GraphicalLassoScene
```

### Quality options

- `-ql`: Low quality (480p, 15fps) - fast for testing
- `-qm`: Medium quality (720p, 30fps)
- `-qh`: High quality (1080p, 60fps)
- `-qk`: 4K quality (2160p, 60fps)

### Use in your own code

```python
import numpy as np
from ggm_viz import GaussianGraphScene

# Create a custom precision matrix
precision_matrix = np.array([
    [1.0, 0.5, 0.0, 0.3],
    [0.5, 1.0, 0.4, 0.0],
    [0.0, 0.4, 1.0, 0.6],
    [0.3, 0.0, 0.6, 1.0]
])

# The scene visualizes the relationship between the precision matrix
# and the corresponding graphical model
```

## Background

### Gaussian Graphical Models

A Gaussian Graphical Model represents the conditional independence structure of a multivariate Gaussian distribution. The key insight is that for a multivariate Gaussian:

- The **precision matrix** Θ = Σ⁻¹ encodes conditional independencies
- Variables Xᵢ and Xⱼ are conditionally independent given all other variables if and only if Θᵢⱼ = 0

### Graphical Lasso

The Graphical Lasso estimates a sparse precision matrix by solving:

$$\hat{\Theta} = \arg\max_{\Theta \succ 0} \left[ \log \det \Theta - \text{tr}(S\Theta) - \lambda \|\Theta\|_1 \right]$$

Where:
- S is the sample covariance matrix
- λ is the regularization parameter
- ‖Θ‖₁ is the L1 norm promoting sparsity

## Development

### Running tests

```bash
pytest tests/
```

### Linting

```bash
ruff check src/ tests/
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.