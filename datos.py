"""Configuración inicial: |V| = 11, |E| = 17.
Cada vértice es una posición/intersección; cada arco, un pasillo de sentido único."""
POS = {"s": (60, 250), "A": (200, 100), "B": (380, 100), "C": (560, 100),
       "D": (200, 250), "E": (380, 250), "F": (560, 250),
       "G": (200, 400), "H": (380, 400), "I": (560, 400), "t": (740, 250)}
ARCOS = [("s", "A"), ("s", "D"), ("s", "G"),
         ("A", "B"), ("B", "C"), ("C", "t"),
         ("D", "E"), ("E", "F"), ("F", "t"),
         ("G", "H"), ("H", "I"), ("I", "t"),
         ("B", "E"), ("E", "H"), ("D", "A"), ("G", "D"), ("F", "C")]
