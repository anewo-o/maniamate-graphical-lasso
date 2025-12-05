from manim import *

class Hypotheses(Scene):

    def construct(self):

        title = Tex("Hypothèses", color=BLUE, font_size=DEFAULT_FONT_SIZE*2)
        self.play(Write(title))
        self.wait(3)
        self.play(title.animate.to_edge(UP))

        ########################################################################

        hypothesis = VGroup(
            MathTex(r"\text{Stabilité du Voisinage : } MSE+\eta \Vert\theta\Vert_1 =MSE" ),
            Tex("Corrélations partielles bornée positvement par le dessous")
        ).arrange(DOWN)
        
        self.play(Write(hypothesis))
        # self.wait(3)
        self.play(Unwrite(hypothesis))

        hypothesis = VGroup(
            MathTex(r"\text{Existence de } \Sigma \text{ : Var}(X_a \mid X_{\Gamma(n)\setminus a}) \geq v^2"),
            Tex("(inversibilité de la covariance, mais pas empirique)").scale(0.7)
        ).arrange(DOWN)
        
        self.play(Write(hypothesis))
        # self.wait(3)
        self.play(Unwrite(hypothesis))

        hypothesis = VGroup(
            MathTex(r"\text{Lasso : Var}(X_a)=1 \text{ et } \Vert\theta^{a,ne_b\setminus a}\Vert_1 \leq \mathcal(\theta)"),
            MathTex(r"\text{Équivalent à : } \max_{b\in ne_a}\left| ne_a\cap ne_b\right|\leq m \text{ (``Sparsity'')}")
        ).arrange(DOWN)

        self.play(Write(hypothesis))
        # self.wait(3)
        self.play(Unwrite(hypothesis))

        ########################################################################

        self.play(Unwrite(title))
        title = Tex("Sparsity", color=BLUE, font_size=DEFAULT_FONT_SIZE*2)
        self.play(
            Write(title),
            title.animate.to_edge(UP)
        )

        hypothesis = VGroup(
            MathTex(r"\max \left|ne_a\right|=O(n^{\kappa}), 0\leq \kappa<1")
        ).arrange(DOWN)

        self.play(Write(hypothesis))
        # self.wait(3)
        self.play(Unwrite(hypothesis))

        ########################################################################

        self.play(Unwrite(title))
        title = Tex("Grandes Dimensions", color=BLUE, font_size=DEFAULT_FONT_SIZE*2)
        self.play(
            Write(title),
            title.animate.to_edge(UP)
        )

        hypothesis = VGroup(
            MathTex(r"p=O(n^\gamma), \gamma>0")
        ).arrange(DOWN)

        self.play(Write(hypothesis))
        # self.wait(3)
        self.play(Unwrite(hypothesis))