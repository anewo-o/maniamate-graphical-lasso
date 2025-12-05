from manim import *
from itertools import combinations

class Partie1Scene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # --- 1) Titre global puis transition ---
        title = Text("Méthodes d'estimation", font_size=42, color=YELLOW)
        title.to_edge(UP)
        self.play(FadeIn(title), run_time=1.5)

        exhaustive_title = Text("Recherche exhaustive", font_size=36, color=WHITE)
        exhaustive_title.to_edge(UP)
        self.play(FadeOut(title), FadeIn(exhaustive_title), run_time=1.5)

        # --- 2) Graphe simple avec 3 nœuds en triangle ---
        nodes = [
            Dot(LEFT*5 + UP*1.5, color=WHITE),
            Dot(LEFT*4 + DOWN*0.5, color=WHITE),
            Dot(LEFT*6 + DOWN*0.5, color=WHITE)
        ]
        graph_simple = VGroup(*nodes)
        self.play(FadeIn(graph_simple), run_time=1.5)

        # --- 3) Flèche vers la droite avec texte ---
        arrow = Arrow(graph_simple.get_right(), RIGHT*2, buff=0.5, color=YELLOW)
        arrow_text = MathTex("\\Sigma^{-1} \\text{ en fonction du graphe}", color=YELLOW).scale(0.7)
        arrow_text.next_to(arrow, UP, buff=0.2)
        self.play(GrowArrow(arrow), Write(arrow_text), run_time=1.5)

        # --- 4) Tableau compact à droite ---
        header = [Text("G_1"), Text("G_2"), MathTex("\\cdots"), Text("G_k")]
        values = [MathTex("v_1"), MathTex("v_2"), MathTex("\\cdots"), MathTex("v_k")]
        table = MobjectTable([header, values], include_outer_lines=True)
        table.scale(0.5).next_to(arrow, RIGHT*1.5)
        table_title = Text("Évaluation du modèle et sélection", font_size=28, color=WHITE).next_to(table, UP)
        self.play(FadeIn(table), FadeIn(table_title), run_time=1.5)

        # --- 5) Tous les graphes possibles se tracent à tour de rôle ---
        # Pour 3 nœuds, il y a 3 arêtes possibles (non orientées)
        possible_edges = [
            (nodes[0], nodes[1]),
            (nodes[1], nodes[2]),
            (nodes[0], nodes[2])
        ]

        all_graphs = []
        for r in range(1, len(possible_edges)+1):
            for combo in combinations(possible_edges, r):
                edges = [Line(e[0].get_center(), e[1].get_center(), color=GREY_B) for e in combo]
                all_graphs.append(VGroup(*edges))

        # Animation : tous les graphes défilent rapidement
        for g in all_graphs[:-1]:  # tous sauf le dernier
            self.play(Create(g), g.animate.set_color(YELLOW), run_time=0.2)
            self.play(FadeOut(g), run_time=0.1)

        # Dernier graphe reste affiché
        last_graph = all_graphs[-1]
        self.play(Create(last_graph), last_graph.animate.set_color(YELLOW), run_time=0.5)

        # --- Flèche vers le bas depuis le tableau ---
        arrow_down = Arrow(table.get_bottom(), table.get_bottom() + DOWN*2, buff=0.2, color=GREEN)
        self.play(GrowArrow(arrow_down), run_time=1)

        # --- Texte en dessous de la flèche ---
        mei_text = Text("modèle G_i sélectionné", font_size=32, color=GREEN)
        mei_text.next_to(arrow_down, DOWN, buff=0.3)
        self.play(Write(mei_text), run_time=2)

        # --- Encadré "Problématique" sous le graphe ---
        problematique_text = VGroup(
            Text("Problématique", font_size=32, color=RED),
            Text("Complexité de l'algorithme exhaustif :", font_size=28, color=WHITE),
            MathTex("2^{\\tfrac{p(p-1)}{2}}", color=YELLOW).scale(0.9)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        problematique_text.next_to(graph_simple, DOWN*2)
        box = SurroundingRectangle(problematique_text, color=RED, buff=0.3)
        problematique_group = VGroup(problematique_text, box)
        problematique_group.shift(RIGHT*3) 

        self.play(FadeIn(problematique_group), run_time=2)
        self.wait(1)

        # --- 1) Tout disparaît (graphe, encadré, tableau, flèches, etc.) ---
        self.play(
            FadeOut(graph_simple),
            FadeOut(last_graph),
            FadeOut(problematique_group),
            FadeOut(table),
            FadeOut(table_title),
            FadeOut(arrow),
            FadeOut(arrow_text),
            FadeOut(arrow_down),
            FadeOut(mei_text),
            FadeOut(exhaustive_title),
            run_time=2
        )


        # --- 1) Titre ---
        mle_title = Text("Maximum de vraisemblance (MLE)", font_size=36, color=WHITE)
        mle_title.to_edge(UP)
        self.play(FadeIn(mle_title), run_time=2)

        # --- 2) Formule de la vraisemblance multivariée (centrée) ---
        likelihood = MathTex(
            "L(\\mu, \\Sigma) = \\prod_{i=1}^n \\frac{1}{(2\\pi)^{d/2} |\\Sigma|^{1/2}}",
            "\\exp\\left(-\\tfrac{1}{2}(x_i - \\mu)^T \\Sigma^{-1}(x_i - \\mu)\\right)"
        ).scale(0.7)
        likelihood.next_to(mle_title, DOWN, buff=1)
        self.play(Write(likelihood), run_time=3)

        # --- 3) Formules à gauche ---
        # mu chapeau
        mu_hat = MathTex("\\hat{\\mu} = \\frac{1}{n} \\sum_{i=1}^n x_i", color=GREEN).scale(0.9)
       

        # sigma chapeau (développé)
        sigma_hat = MathTex(
            "\\hat{\\Sigma} = \\frac{1}{n} \\sum_{i=1}^n (x_i - \\hat{\\mu})(x_i - \\hat{\\mu})^T=\\frac{1}{n} X^T X ",
            color=BLUE
        ).scale(0.9)
    

        # Les mettre en colonne (sigma sous mu)
        formulas = VGroup(mu_hat, sigma_hat).arrange(DOWN, buff=0.6)

        # Position initiale : au centre sous la vraisemblance
        formulas.next_to(likelihood, DOWN, buff=1)
        self.play(Write(mu_hat), run_time=1.5)
        self.play(Write(sigma_hat), run_time=1.5)

        self.wait(1)

        # --- Déplacement du bloc vers la gauche ---
        self.play(formulas.animate.to_edge(LEFT).shift(DOWN*0.5), run_time=2)
        self.wait(1)
        # --- Encadré "Problématique" à droite ---
        problematique_text = VGroup(
            Text("Problématique", font_size=32, color=RED),
            MathTex("Taille\\  de\\ \\hat{\\Sigma} = p \\times p", font_size=28, color=WHITE),
            MathTex("Rang\\ de\\ \\hat{\\Sigma} = n", font_size=28, color=WHITE),
            MathTex("Or\\  n << p  \\rightarrow  \\hat{\\Sigma}\\  non-inversible", font_size=28, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        problematique_text.to_edge(RIGHT).shift(DOWN*0.5)
        box = SurroundingRectangle(problematique_text, color=RED, buff=0.3)
        problematique_group = VGroup(problematique_text, box)

        self.play(FadeIn(problematique_group), run_time=2)

        self.wait(3)
