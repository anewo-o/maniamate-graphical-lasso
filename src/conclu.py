from manim import *

class Conclusion(Scene):

    def construct(self):
        
        title = Tex("Conclusion", color=BLUE, font_size=DEFAULT_FONT_SIZE*2)
        self.play(Write(title)) ; self.wait(3)
        self.play(title.animate.to_edge(UP, buff=LARGE_BUFF))

        complexity = Tex(
            r"D'une complexité exhaustive exponentielle \\" \
            r"à une complexité quadratique."
        )
        
        self.play(Write(complexity)) ; self.wait(3)
        self.play(complexity.animate.next_to(title, DOWN, buff=MED_LARGE_BUFF))

        control = VGroup(
            MathTex(r"\text{Contrôle d'erreur de type I et II}\\"),
            MathTex(r"\mathbb{P}(\hat ne_a^{\lambda} \subseteq ne_a) = 1 - O(\exp(-cn^\epsilon))"),
            MathTex(r"\mathbb{P}(ne_a \subseteq \hat ne_a^{\lambda}) = 1 - O(\exp(-cn^\epsilon))"),
            MathTex(r"\epsilon \geq 1").scale(0.7)
        ).arrange(DOWN)

        self.play(
            Write(control),
            control.animate.next_to(complexity, DOWN, buff=MED_LARGE_BUFF),
            run_time=3
        ) ; self.wait(3)

        
        