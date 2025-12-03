# Manim Community v0.18+ recommended
# Run example:
# manim -pql gene_lasso_video.py IntroScene Part1Scene Part2Scene Part3Scene ConclusionScene
#
# Notes:
# - This script focuses ONLY on visuals (no narration/audio).
# - Timings are approximate; adjust run_time values to fit your 1.5–2.5 min sections.
# - You can freely modify colors, positions, pacing, and graph sizes.
# - Helper functions at bottom centralize repeated visual logic.
# - If your Manim version differs, minor API changes may be necessary.

from manim import *
import numpy as np
import itertools
import random

# Global style constants (tweak to your taste)
PRIMARY_COLOR = YELLOW
SECONDARY_COLOR = BLUE
HIGHLIGHT_COLOR = RED
GRAPH_NODE_COLOR = WHITE
GRAPH_EDGE_COLOR = GREY_B
ZERO_HL_COLOR = GREEN
NONZERO_HL_COLOR = ORANGE
DIVINE_GLOW_COLOR = GOLD
BG_COLOR = BLACK

# Graph config
DEFAULT_P = 6  # number of genes/nodes in small examples
LARGE_P = 10   # larger example for exhaustive search "too long"
NODE_RADIUS = 0.2

# Matrix text style
MATRIX_FONT_SIZE = 28
TITLE_FONT_SIZE = 36
LABEL_FONT_SIZE = 28

# ------------------------------------------------------------
# INTRO (~1’30)
# ------------------------------------------------------------
class IntroScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- 1) Quelques secondes de noir ---
        self.wait(2)

     # Tableau avec en-tête "gène1 ... gène p"
        header = [Text(f"gène {j}") for j in range(1,6)]
        rows = [[MathTex(f"x_{{{i},{j}}}") for j in range(1,6)] for i in range(1,6)]
        table = MobjectTable([header] + rows, include_outer_lines=True)
        table.scale(0.35)        # taille fixée dès le départ
        table.move_to(ORIGIN)   # centré


        brace_p = Brace(table, UP)
        label_p = brace_p.get_text("p gènes")

        # Accolade verticale uniquement sur les lignes de données
        rows_only = VGroup(*table.get_rows()[1:])  # saute l'en-tête
        brace_n = Brace(rows_only, LEFT)
        brace_n.shift(LEFT*0.4)
        label_n = brace_n.get_text("n données")

        # Regrouper tout dans un seul bloc
        table_block = VGroup(table, brace_p, label_p, brace_n, label_n)

        # Animation
        self.play(FadeIn(table_block), run_time=2)

        self.wait(1)

        # --- 3) Tableau se réduit vers la gauche + flèche + graphe ---
        self.play(table_block.animate.scale(0.7).to_edge(LEFT), 
                  run_time=2)

        arrow = Arrow(table.get_right(), table.get_right() + RIGHT*3.5, buff=0.5, color=YELLOW)

        self.play(GrowArrow(arrow), run_time=1)

        # Graphe à droite du tableau (pas superposé à la flèche)
        num_nodes = 10
        nodes = []
        positions = []
        radius = 2.0

        # Placer les nœuds en cercle
        for k in range(num_nodes):
            theta = 2*np.pi*k/num_nodes
            x = radius*np.cos(theta) + 4.0
            y = radius*np.sin(theta)
            pos = np.array([x, y, 0])
            positions.append(pos)
            c = Dot(pos, color=WHITE)
            nodes.append(c)

        nodes_group = VGroup(*nodes)
        self.play(FadeIn(nodes_group), run_time=2)

        # Définir une liste fixe de connexions (non symétrique)
        connections = [
            (0,1),(0,3),(0,7),(0, 6),      # nœud 0 relié à 3 voisins
            (1,2),(1,5),            # nœud 1 relié à 2 voisins
            (2,4),(2,8),(2,9),      # nœud 2 relié à 3 voisins
            (3,6),(3,4),                  # nœud 3 relié à 2 voisins (0 et 6)
            (4,5),(4,7),            # nœud 4 relié à 3 voisins
            (5,9),                  # nœud 5 relié à 3 voisins (1,4,9)
            (6,8),                  # nœud 6 relié à 2 voisins (3,8)
            (7,9),                  # nœud 7 relié à 3 voisins (0,4,9)
            (8,9)                   # nœud 8 relié à 3 voisins (2,6,9)
        ]

        # Créer les arêtes
        edges = []
        for i,j in connections:
            e = Line(positions[i], positions[j], color=GREY_B, stroke_width=1)
            edges.append(e)

        edges_group = VGroup(*edges)
        self.play(LaggedStartMap(Create, edges_group, lag_ratio=0.1, run_time=4))

       

        self.wait(1)

        # --- 4) Tableau et flèche disparaissent, graphe à gauche + loi et matrice à droite ---
        self.play(FadeOut(table), FadeOut(brace_p), FadeOut(label_p),
                  FadeOut(brace_n), FadeOut(label_n), FadeOut(arrow), run_time=1)

        self.play(nodes_group.animate.shift(LEFT*8), edges_group.animate.shift(LEFT*8), run_time=2)


        law = MathTex("X \\sim \\mathcal{N}(\\mu, \\Sigma)", color=YELLOW)
        law.to_edge(RIGHT, buff=3).shift(UP*0.5)
        precision = MathTex("\\Omega = \\Sigma^{-1}", color=RED)
        precision.next_to(law, DOWN)

        self.play(Write(law), Write(precision), run_time=2)

        # --- 5) Réapparition tableau + flèche + graphe à droite + loi et matrice réduites en bas ---
        law_small = law.copy().scale(0.7).to_edge(DOWN).shift(LEFT*2)
        precision_small = precision.copy().scale(0.7).next_to(law_small, RIGHT)

        self.play(FadeOut(law), FadeOut(precision), FadeIn(law_small), FadeIn(precision_small))

        # Graphe revient à droite
        self.play(nodes_group.animate.to_edge(RIGHT), edges_group.animate.to_edge(RIGHT), run_time=2)

        # Tableau et flèche se replacent
        self.play(FadeIn(table), FadeIn(brace_p), FadeIn(label_p),
                  FadeIn(brace_n), FadeIn(label_n), FadeIn(arrow), run_time=2)

        # Point d’interrogation au-dessus de la flèche
        qm = Text("?", font_size=72, color=RED).next_to(arrow, UP, buff=0.5)
        self.play(FadeIn(qm), run_time=1)

        self.wait(2)


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def create_circular_nodes(num=6, radius=3.0, node_radius=0.2, color=WHITE):
    """
    Create `num` Circular nodes placed evenly on a circle.
    Returns list of Circle mobjects.
    """
    nodes = []
    for k in range(num):
        angle = 2 * np.pi * k / num
        pos = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
        c = Circle(radius=node_radius, color=color)
        c.set_fill(color, opacity=1.0)
        c.move_to(pos)
        nodes.append(c)
    return nodes

def build_graph_layout(scene, n=8, origin_shift=ORIGIN, node_color=WHITE, radius=3.0):
    """
    Create a graph layout with n circular nodes and return dict:
    { 'nodes': VGroup, 'pos': list of positions }
    """
    nodes = create_circular_nodes(num=n, radius=radius, node_radius=NODE_RADIUS, color=node_color)
    nodes_group = VGroup(*nodes).shift(origin_shift)
    pos = [node.get_center() for node in nodes]
    return {"nodes": nodes_group, "pos": pos}

def sample_possible_edges(p, k=10):
    """
    Sample k distinct undirected edges (i<j) out of p nodes.
    Used to simulate exhaustive testing.
    """
    all_pairs = [(i, j) for i in range(p) for j in range(i+1, p)]
    random.shuffle(all_pairs)
    return all_pairs[:k]

def draw_schematic_matrix(rows=6, cols=6, font_size=28, dotted_border=False):
    """
    Create a schematic matrix as a grid of small squares and labels.
    If dotted_border=True, emphasize border with dashed rectangles.
    """
    squares = []
    for i in range(rows):
        for j in range(cols):
            sq = Square(side_length=0.35, color=GREY_B)
            sq.set_fill(GREY_E, opacity=0.2)
            sq.move_to(np.array([0.2*(j - cols/2), -0.2*(i - rows/2), 0]))
            squares.append(sq)
    mat = VGroup(*squares).scale(1.2)

    if dotted_border:
        rect = Rectangle(width=0.2*cols, height=0.2*rows, color=GREY_B).scale(1.2)
        rect.set_stroke(GREY_A, width=2, opacity=0.6)
        mat = VGroup(mat, rect)
    return mat

def draw_precision_matrix_with_zeros(p, font_size=28):
    """
    Build a schematic precision matrix Ω showing zeros and non-zeros.
    Simple heuristic: diagonal non-zero, off-diagonal sparse random zeros/non-zeros.
    """
    squares = []
    labels = []
    for i in range(p):
        for j in range(p):
            sq = Square(side_length=0.38, color=GREY_B)
            sq.set_fill(GREY_E, opacity=0.2)
            sq.move_to(np.array([0.45*(j - p/2), -0.45*(i - p/2), 0]))
            squares.append(sq)

            # Heuristic: diagonal always nonzero, off-diagonal random zero/nonzero
            if i == j:
                val = "•"  # indicates non-zero diagonal
                color = WHITE
            else:
                # Randomly choose zero/non-zero
                if random.random() < 0.7:
                    val = "0"
                    color = ZERO_HL_COLOR
                else:
                    val = "×"
                    color = NONZERO_HL_COLOR
            label = Text(val, font_size=font_size, color=color).move_to(sq.get_center())
            labels.append(label)
    return VGroup(*squares, *labels)

def highlight_precision_entries(precision_group, zero_color=GREEN, nz_color=ORANGE):
    """
    Create overlay rectangles on zeros and non-zeros in a precision matrix group.
    Assumes Text labels "0" and "×" inside the group.
    Returns (zero_rects, nonzero_rects) VGroups.
    """
    zero_rects = []
    nonzero_rects = []
    for mobj in precision_group:
        if isinstance(mobj, Text):
            val = mobj.text
            if val == "0":
                r = SurroundingRectangle(mobj, color=zero_color, buff=0.03)
                zero_rects.append(r)
            elif val == "×":
                r = SurroundingRectangle(mobj, color=nz_color, buff=0.03)
                nonzero_rects.append(r)
    return VGroup(*zero_rects), VGroup(*nonzero_rects)

def synthetic_nonzero_pairs(p, density=0.3):
    """
    Create synthetic undirected edge pairs representing nonzero off-diagonal entries.
    """
    pairs = []
    for i in range(p):
        for j in range(i+1, p):
            if random.random() < density:
                pairs.append((i, j))
    return pairs

def draw_edges_from_pairs(nodes, pairs, edge_color=GREY_B):
    """
    Draw edges for given pairs among nodes.
    """
    edges = []
    for (i, j) in pairs:
        e = Line(nodes[i].get_center(), nodes[j].get_center(), color=edge_color)
        edges.append(e)
    return VGroup(*edges)

def apply_rule(pairs, rule="AND"):
    """
    Placeholder for neighborhood combination rule.
    Since we don't have separate directional neighborhoods in this visual,
    we just return the same pairs and tint differently to illustrate the idea.
    """
    # In real logic, 'AND' would intersect neighborhoods, 'OR' would union them.
    return pairs

def draw_data_matrix(n=20, p=6, font_size=24):
    """
    Draw a schematic data matrix X of shape (n x p).
    """
    cells = []
    for i in range(n):
        for j in range(p):
            sq = Square(side_length=0.25, color=GREY_B)
            sq.set_fill(GREY_E, opacity=0.2)
            sq.move_to(np.array([0.3*(j - p/2), -0.24*(i - n/2), 0]))
            cells.append(sq)
    label = Text("X (n×p)", font_size=font_size, color=WHITE)
    mat = VGroup(*cells).scale(1.1)
    return VGroup(label.next_to(mat, UP), mat)

def highlight_row_col(matrix_group, idx=0, nz_fraction=0.3):
    """
    Highlight entries in a row and column of a schematic matrix as if updating Ω.
    """
    rects = []
    # Collect Text entries, estimate grid coordinates by their spatial positions
    texts = [m for m in matrix_group if isinstance(m, Text)]
    if not texts:
        return VGroup()

    # Infer positions to find the row/col for the given idx
    # For simplicity we assume p = sqrt(len(texts)) (since we built square grid).
    p = int(np.sqrt(len(texts)))
    # Sort by y, then by x to create row-major ordering
    texts_sorted = sorted(texts, key=lambda t: (-t.get_center()[1], t.get_center()[0]))
    # Convert to 2D list
    grid = [texts_sorted[i*p:(i+1)*p] for i in range(p)]

    # Highlight row idx
    for j in range(p):
        r = SurroundingRectangle(grid[idx][j], color=ORANGE, buff=0.03)
        rects.append(r)
    # Highlight col idx
    for i in range(p):
        r = SurroundingRectangle(grid[i][idx], color=ORANGE, buff=0.03)
        rects.append(r)

    return VGroup(*rects)
