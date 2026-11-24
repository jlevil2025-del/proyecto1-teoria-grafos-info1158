"""
Verificación (sección 5 del enunciado).
Caso manual de 5 vértices, resuelto a mano:
  Arcos: s->a, s->b, a->b, a->t, b->c, b->t, c->t
  Camino mínimo: s->a->t (2 arcos). No hay arco directo s->t y s no tiene otro vecino que a y b,
  por lo que no existe camino de longitud 1.
  Caminos sin arcos compartidos: s->a->t y s->b->t (2 caminos).
  Corte de igual tamaño: {s->a, s->b} (2 arcos). Como 2 = 2, la familia es máxima y el corte mínimo.
"""
from algoritmos import Grafo, resolver
from datos import POS, ARCOS

g = Grafo(["s", "a", "b", "c", "t"],
          [("s", "a"), ("s", "b"), ("a", "b"), ("a", "t"), ("b", "c"), ("b", "t"), ("c", "t")])
r = resolver(g, "s", "t")
print("Caso manual:", r["distancia"], r["k"], r["corte"])
assert r["distancia"] == 2 and r["k"] == 2 and set(r["corte"]) == {("s", "a"), ("s", "b")}
assert all(ok for _, ok in r["verificacion"])

g_prueba = Grafo(["a", "b"], [("a", "b")])
g_prueba.alternar_bloqueo(("a", "b"))
g_prueba.eliminar_arco(("a", "b"))
assert g_prueba.arcos == [] and g_prueba.bloqueados == set()

r = resolver(Grafo(POS.keys(), ARCOS), "s", "t")
print("Red principal:", r["distancia"], r["k"], r["corte"])
assert all(ok for _, ok in r["verificacion"])
print("Todas las verificaciones OK")
