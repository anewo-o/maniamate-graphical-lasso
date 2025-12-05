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
        ) 

        self.play(FadeOut(complexity), FadeOut(control), run_time=2)
        # --- Les 4 points ---
        point1 = Text("Un même λ masque les hubs dans un réseau hétérogène.",
                      font_size=28, color=WHITE).next_to(title, DOWN, buff=1).align_to(title, LEFT)
        point2 = Text("Le choix du paramètre λ est critique :\n   mal choisi, on rate des voisins ou on prend du bruit.",
                      font_size=28, color=WHITE).next_to(point1, DOWN, buff=0.6).align_to(point1, LEFT)
        point3 = Text("Chaque nœud est traité séparément :\n   la symétrie n’est pas garantie (bricolage AND/OR).",
                      font_size=28, color=WHITE).next_to(point2, DOWN, buff=0.6).align_to(point1, LEFT)

        # Regrouper et centrer la liste
        points = VGroup(point1, point2, point3).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        points.move_to(ORIGIN)  # centre la liste sur l'écran

        # --- Animation cumulative ---
        self.play(Write(point1), run_time=2)
        self.wait(1)
        self.play(Write(point2), run_time=2)
        self.wait(1)
        self.play(Write(point3), run_time=2)
        self.wait(1)

        #---Réduction des points à gauche de l'écran + flèche ---
                # --- Réduction + placement très à gauche ---
        self.play(
            points.animate.scale(0.7).to_edge(LEFT, buff=0.05),
            run_time=2
        )

        # --- Flèche partant du bord droit des points ---
        arrow = Arrow(
            start=points.get_right(),              # bord droit du bloc de points
            end=points.get_right() + RIGHT*4,      # prolongement vers la droite
            color=YELLOW,
            stroke_width=6
        )
        self.play(GrowArrow(arrow), run_time=2)

        # --- Texte "Graphical Lasso" au bout de la flèche ---
        glasso_text = Text("Graphical Lasso", font_size=32, color=YELLOW)
        glasso_text.next_to(arrow.get_end(), RIGHT, buff=0.3)  # aligné horizontalement au bout
        self.play(Write(glasso_text), run_time=2)

        self.wait(2)
        #---- Fin de la scène principale ----#
        self.play(FadeOut(points), FadeOut(title), FadeOut(arrow), FadeOut(glasso_text), run_time=2)  
        # --- Générique défilant ---
        scroll_text = VGroup(
            Text("Réalisé par :", font_size=32, color=WHITE, font="Arial Bold"),
            Text("Athur Lamazière", font_size=28, color=WHITE),
            Text("Owen Couturier", font_size=28, color=WHITE),
            Text("Maelle Luzurier", font_size=28, color=WHITE),
            Text("Titouan Choaler", font_size=28, color=WHITE),
            Text("Article source : ", font_size=32, color=WHITE, font="Arial Bold"),
            Text("'High dimensional graphs and\n variable selection with the Lasso'", font_size=32, color=WHITE),
            Text("Nicolai Meinshausen et Peter Bühlmann", font_size=28, color=WHITE)
        ).arrange(DOWN, buff=0.6)

        # Position initiale : bien en bas (hors champ)
        scroll_text.move_to(DOWN*7)

        # Animation : défilement vers le haut (hors champ)
        self.play(scroll_text.animate.move_to(UP*8), run_time=12, rate_func=linear)
       
        
