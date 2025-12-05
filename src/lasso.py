"""
Visualization module for Gaussian Graphical Models.
"""

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

