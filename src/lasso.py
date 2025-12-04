"""
Visualization module for Gaussian Graphical Models.
"""

import networkx as nx
import numpy as np
from manim import *


class LassoIntroduction(Scene):
    """
    Introducing the Lasso regularization.
    """

    def construct(self):
        """
        Scene construction in sequence.
        """

        ########################################################################
        ### Lasso Halo #########################################################
        ########################################################################

        lasso = Text("Lasso", color=BLUE, font_size=DEFAULT_FONT_SIZE*2)
        self.play(Write(lasso))

        halo = Ellipse(
            width=5.3,
            height=2.3,
            color=YELLOW,
            fill_opacity=0.4,
            stroke_opacity=0.2
        ).move_to(lasso)
        halo.set_z_index(1)
        self.play(FadeIn(halo), run_time=3)
        self.play(FadeOut(halo), run_time=1)
        
        self.play(lasso.animate.to_edge(UP))

        ########################################################################
        ### Propriété de la pénalité ###########################################
        ########################################################################

        penalty = MathTex(
            r"\text{Pénalité Lasso: } \lambda \sum_{b=1}^{p} \lvert \theta_b^a \rvert",
            font_size=DEFAULT_FONT_SIZE,
            color=WHITE
        ).next_to(lasso, DOWN, buff=1)
        self.play(FadeIn(penalty))
        self.wait(2)

        bullets = BulletedList(
            r"Introduit biais, réduit variance",
            r"Régularisation des coefficients",
            r"Dont certains deviennent \underline{nuls}",
            font_size=DEFAULT_FONT_SIZE*0.8,
            dot_scale_factor=1.2,
            buff=0.3,
        ).next_to(
            penalty,
            DOWN
        ).align_to(
            penalty,
            LEFT,
        )

        self.play(FadeIn(bullets))
        self.wait(2)
        self.play(FadeOut(bullets))

        self.play(FadeOut(penalty), runtime=2)

        full = MathTex(
            r"\hat{\theta}^{\,a,\lambda}\
            = \arg\min_{\theta :\, \theta_a = 0}\
            \left( n^{-1} \| X_a - X\theta \|_2^{2}+ \lambda \|\theta\|_{1} \right)",
            font_size=DEFAULT_FONT_SIZE,
            color=WHITE
        )
        self.play(FadeIn(full))

        self.play(full.animate.next_to(lasso, DOWN).scale(0.7))


        ########################################################################
        ### Parcimonie et norme 1 ##############################################
        ########################################################################

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY_B},
            background_line_style={"stroke_opacity": 0.3}
        ).next_to(full,DOWN)
        self.play(Create(plane))

        diamond = Polygon(
            [0, 2, 0],
            [2, 0, 0],
            [0, -2, 0],
            [-2, 0, 0],
            color=BLUE,
            fill_opacity=0.2,
            stroke_width=4
        ).move_to(plane)

        ellipse = Ellipse(
            width=3,
            height=2,
            color=PURPLE,
            fill_opacity=0.1,
            stroke_width=4
        ).next_to(diamond, RIGHT, buff=-0.15).rotate(PI/6, axis=OUT)

        touch = Dot(color=YELLOW).move_to(diamond.get_right())

        self.play(Create(diamond))
        self.play(Create(ellipse))
        self.play(FadeIn(touch))

        labels = VGroup(
            MathTex(
                r"\lambda\Vert\theta\Vert_1", 
                font_size=DEFAULT_FONT_SIZE*0.6,
                color=BLUE
            ).next_to(diamond, UP, buff=0.4),
            Tex(
                r"Niveau de MSE", 
                font_size=DEFAULT_FONT_SIZE*0.6,
                color=PURPLE
            ).next_to(ellipse, UP, buff=0.4),
            MathTex(
                r"\text{Intersection} \\",
                r"\text{au minimum} \\",
                r"\theta=(2,0)", 
                font_size=DEFAULT_FONT_SIZE*0.6,
                color=YELLOW
            ).next_to(touch, LEFT, buff=0.2)
        )
        self.play(FadeIn(labels))
        self.wait(2)


class LassoNeighborhood(Scene):
    """
    Neighborhood Graph Construction
    """

    def construct(self):
        title = Tex("Algorithme de Sélection", color=BLUE, font_size=DEFAULT_FONT_SIZE*2)
        
        self.play(Write(title))
        self.wait(3)
        self.play(title.animate.scale(0.7).to_edge(UP))

        ########################################################################
        ### Initialisation du graphe ###########################################
        ########################################################################

        nodes = 8
        graph = Graph(
            vertices = list(range(nodes)),
            edges=[],
            layout="circular",
            labels=True,
            label_fill_color=BLUE,
        )

        self.play(Create(graph))
        self.wait(2)
        self.play(Unwrite(title), run_time=1)


        ########################################################################
        ### Voisinage de 0 #####################################################
        ########################################################################

        title = MathTex("ne_0", color=BLUE, font_size=DEFAULT_FONT_SIZE*2).to_edge(UP)
        self.play(Write(title))

        ne_0 = [(0, 1), (0, 2), (0, 4), (0, 6)]
        for edge in ne_0:
            graph.add_edges(edge)
            self.play(Create(graph.edges[edge]), run_time=1)

        self.wait(2)
        self.play(Unwrite(title))


        ########################################################################
        ### Voisinage de 1 #####################################################
        ########################################################################

        title = MathTex("ne_1", color=BLUE, font_size=DEFAULT_FONT_SIZE*2).to_edge(UP)

        self.play(Write(title),
                  graph.animate.to_edge(LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER*4)
        )

        equations = VGroup(
            MathTex(r"X_0=\theta_1^0X_1+\theta_2^0X_2+0X_3..."),
            MathTex(r"X_1=\theta_0^1X_0+\theta_2^1X_2+0X_4..."),
            MathTex(r"\theta_1^0 \neq 0 \Rightarrow X_1 \in ne_0"),
            MathTex(r"\textbf{et } \theta_0^1 \neq 0 \Rightarrow X_0 \in ne_1"),
            MathTex(r"\text{donc } (0,1)\in \hat E^{\land}")
        ).arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)

        graph.add_edges((1,0), edge_config={"stroke_color":GREEN})
        self.play(
            ShowPassingFlash(
                graph.edges[(1,0)].copy().set_stroke(width=DEFAULT_STROKE_WIDTH*3),
                time_width=0.3,
            ), FadeOut(graph.edges[(1,0)]),
            FadeIn(equations.next_to(graph, RIGHT).scale(0.7)),
            run_time=3
        )

        self.wait(2)

        ne_1 = [(1, 2), (1, 3), (1, 6)]
        for edge in ne_1:
            graph.add_edges(edge)
            self.play(Create(graph.edges[edge]), run_time=1)

        self.wait(2)
        self.play(Unwrite(title),FadeOut(equations))


        ########################################################################
        ### Voisinage de 2 #####################################################
        ########################################################################

        title = MathTex("ne_2", color=BLUE, font_size=DEFAULT_FONT_SIZE*2).to_edge(UP)
        self.play(Write(title))

        equations = VGroup(
            MathTex(r"X_1=\theta_0^1X_0+\theta_2^1X_2+0X_4..."),
            MathTex(r"X_2=0X_0+\theta_1^2X_1+0X_3..."),
            MathTex(r"\theta_2^1 \neq 0\Rightarrow X_2 \in ne_1"),
            MathTex(r"\textbf{mais } \theta_1^2 = 0 \Rightarrow X_1 \notin ne_2"),
            MathTex(r"\text{donc } (0,2) \in \hat E^{\lor}")
        ).arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)

        graph.add_edges((2,1), edge_config={"stroke_color":GREEN})
        self.play(
            ShowPassingFlash(
                graph.edges[(2,1)].copy().set_stroke(width=DEFAULT_STROKE_WIDTH*3),
                time_width=0.3
            ), FadeOut(graph.edges[(2,1)]),
            run_time=3
        )

        graph.add_edges((2,0), edge_config={"stroke_color":RED})
        self.play(
            ShowPassingFlash(
                graph.edges[(2,0)].copy().set_stroke(width=DEFAULT_STROKE_WIDTH*3),
                time_width=0.3
            ), FadeOut(graph.edges[(2,0)]),
            FadeIn(equations.next_to(graph, RIGHT).scale(0.7)),
            run_time=3
        )

        self.wait(2)
        self.play(FadeOut(equations))

        precision = Matrix(
            [
                [r"\theta_0^0", r"\theta_1^0", r"\theta_2^0", r"\cdots"],
                [r"\theta_0^1", r"\theta_1^1", r"\theta_2^1", r"\cdots"],
                [0, r"\theta_1^2", r"\theta_2^2", r"\cdots"],
                [r"\vdots", r"\vdots", r"\vdots", r"\ddots"],
            ],
        )

        pgroup = VGroup(precision,
            MathTex(r"\text{Matrice de précision } K=\Sigma^{-1}", color=BLUE),
            MathTex(r"\text{mais } K \neq K^T", color=WHITE),
        ).arrange(DOWN).next_to(graph,RIGHT).scale(0.8)

        self.play(FadeIn(pgroup))
        self.wait(2)

        ne_2 = [(2, 4), (2, 5), (2, 7)]
        for edge in ne_2:
            graph.add_edges(edge)
            self.play(Create(graph.edges[edge]), run_time=1)

        self.wait(2)
        self.play(Unwrite(title))


        ########################################################################
        ### Voisinages restants ################################################
        ########################################################################

        title = MathTex("...", color=BLUE, font_size=DEFAULT_FONT_SIZE*2).to_edge(UP)
        self.play(Write(title))

        ne_ = [(3,6), (7,5), (6,4)]
        for edge in ne_:
            graph.add_edges(edge)
            self.play(Create(graph.edges[edge]))

        self.wait(2)

