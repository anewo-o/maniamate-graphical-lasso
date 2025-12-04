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
        # --- Titre en haut ---
        title = Text("Réseaux de gènes", font_size=48, color=YELLOW)
        title.to_edge(UP)  # positionné en haut de l’écran
        self.play(FadeIn(title), run_time=2)

        # --- 2) Tableau avec en-tête "gène1 ... gène p" ---
        header = [Text(f"gène {j}") for j in range(1,6)]
        rows = [[MathTex(f"x_{{{i},{j}}}") for j in range(1,6)] for i in range(1,6)]
        table = MobjectTable([header] + rows, include_outer_lines=True)
        table.scale(0.35).move_to(ORIGIN)

        brace_p = Brace(table, UP)
        label_p = brace_p.get_text("p gènes")

        rows_only = VGroup(*table.get_rows()[1:])  # saute l'en-tête
        brace_n = Brace(rows_only, LEFT).shift(LEFT*0.4)
        label_n = brace_n.get_text("n données")

        # Regrouper tout dans un seul bloc 
        table_block = VGroup(table, brace_p, label_p, brace_n, label_n)
        # --- Tableau apparait seul ---
        self.play(FadeIn(table), run_time=2)
        # --- Puis les accolades ---
        self.play(GrowFromCenter(brace_p), FadeIn(label_p),
                  GrowFromCenter(brace_n), FadeIn(label_n), run_time=2)

        self.wait(1)

        # --- 3) Tableau se réduit vers la gauche + flèche + graphe ---
        self.play(table_block.animate.scale(0.7).to_edge(LEFT), run_time=2)

        arrow = Arrow(table_block.get_right(), table_block.get_right() + RIGHT*3, buff=0.5, color=YELLOW)
        self.play(GrowArrow(arrow), run_time=1)

        # Graphe à droite du tableau
        num_nodes = 10
        nodes = []
        positions = []
        radius = 2.0
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

        # Connexions fixes non symétriques
        connections = [
            (0,1),(0,3),(0,7),(0,6),
            (1,2),(1,5),
            (2,4),(2,8),(2,9),
            (3,6),(3,4),
            (4,5),(4,7),
            (5,9),
            (6,8),
            (7,9),
            (8,9)
        ]

        edges = []
        for i,j in connections:
            e = Line(positions[i], positions[j], color=GREY_B, stroke_width=1)
            edges.append(e)

        edges_group = VGroup(*edges)
        self.play(LaggedStartMap(Create, edges_group, lag_ratio=0.1, run_time=4))

        self.wait(1)

        # --- 4) Tableau et flèche disparaissent, graphe à gauche + loi ---
        self.play(FadeOut(table), FadeOut(brace_p), FadeOut(label_p),
                  FadeOut(brace_n), FadeOut(label_n), FadeOut(arrow), run_time=1)

        self.play(nodes_group.animate.shift(LEFT*8), edges_group.animate.shift(LEFT*8), run_time=2)

        # Loi gaussienne
        law = MathTex("X \\sim \\mathcal{N}(\\mu, \\Sigma)", color=YELLOW)
        law.to_edge(RIGHT, buff=1.5).shift(UP*0.5)
        self.play(Write(law), run_time=2)

        # Flèche d’un nœud vers le X
        arrow_to_X = Arrow(nodes[0].get_center(), law[0][0].get_center(), buff=0.5, color=YELLOW)
        self.play(GrowArrow(arrow_to_X), run_time=1)

        # Transformation du X en vecteur gènes
        vector = MathTex("\\begin{bmatrix} g_1 \\\\ g_2 \\\\ \\vdots \\\\ g_p \\end{bmatrix}", color=YELLOW)
        vector.move_to(law[0][0].get_center())
        self.play(Transform(law[0][0], vector), run_time=2)
        self.wait(2)
        # Retour au X
        X_symbol = MathTex("X", color=YELLOW).move_to(vector.get_center())
        self.play(Transform(law[0][0], X_symbol), run_time=2)

        # Flèche disparaît
        self.play(FadeOut(arrow_to_X), run_time=1)

        # Matrice apparait
        precision = MathTex("\\Omega = \\Sigma^{-1}", color=RED)
        precision.next_to(law, DOWN)
        self.play(Write(precision), run_time=2)
        # Matrice Sigma apparait en dessous
        sigma_matrix = MathTex(
            "\\Sigma = \\begin{bmatrix}"
            "\\sigma_{11} & \\sigma_{12} & \\cdots & \\sigma_{1p} \\\\"
            "\\sigma_{21} & \\sigma_{22} & \\cdots & \\sigma_{2p} \\\\"
            "\\vdots & \\vdots & \\ddots & \\vdots \\\\"
            "\\sigma_{p1} & \\sigma_{p2} & \\cdots & \\sigma_{pp}"
            "\\end{bmatrix}",
            color=WHITE
        )
        sigma_matrix.next_to(precision, DOWN*2)
        arrow_sigma = Arrow(precision.get_bottom(), sigma_matrix.get_top(), buff=0.3, color=YELLOW)
        self.play(GrowArrow(arrow_sigma), run_time=1)
        self.play(Write(sigma_matrix), run_time=2)

        start_point = sigma_matrix.get_corner(UL)
        end_point = nodes_group.get_right() + RIGHT*0.5  # vise un peu avant le graphe
        arrow_graph = Arrow(start_point, end_point, buff=0.2, color=RED)
        self.play(GrowArrow(arrow_graph), run_time=1)


        equivalence = MathTex(
            "\\text{arête }(i,j) \\iff \\sigma_{ij} \\neq 0",
            color=RED
        ).scale(0.7)

        equivalence.next_to(arrow_graph, UP, buff=0.2, aligned_edge=LEFT)
        self.play(Write(equivalence), run_time=2)


        self.wait(2)

        self.play(
            FadeOut(arrow_graph),
            FadeOut(equivalence),
            FadeOut(sigma_matrix),
            FadeOut(arrow_sigma),
            run_time=2
        )

        # --- 5) Mouvement fluide vers position centrée ---
        self.play(
            law.animate.scale(0.7).move_to(DOWN*3 + LEFT*2),
            precision.animate.scale(0.7).move_to(DOWN*3 + LEFT*2+RIGHT*3),
            run_time=2
        )

        # Graphe revient à droite
        self.play(nodes_group.animate.to_edge(RIGHT), edges_group.animate.to_edge(RIGHT), run_time=2)

        # Tableau et flèche se replacent
        arrow = Arrow(table_block.get_right(), table_block.get_right() + RIGHT*3, buff=0.5, color=YELLOW)
        self.play(FadeIn(table_block), FadeIn(arrow), run_time=2)

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
