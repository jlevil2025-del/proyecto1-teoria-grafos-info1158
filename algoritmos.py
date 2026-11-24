"""
Proyecto 1 - Teoría de Grafos (INFO1158)
Algoritmos propios, sin bibliotecas externas:
  1. BFS: camino con el menor número de arcos.
  2. Flujo máximo con capacidad 1 por arco (Edmonds-Karp): máximo de caminos sin arcos compartidos.
  3. Corte mínimo de arcos (teorema de Menger / flujo máximo-corte mínimo).
"""
from collections import deque


class Grafo:
    """Grafo dirigido G=(V,E) sin lazos, arcos repetidos ni arcos recíprocos.
    Un arco 'bloqueado' sigue existiendo en E, pero no se usa al calcular."""

    def __init__(self, vertices, arcos=()):
        self.vertices = list(vertices)
        self.arcos = []            # lista de tuplas (u, v)
        self.bloqueados = set()    # arcos desactivados
        for u, v in arcos:
            self.agregar_arco(u, v)

    def agregar_arco(self, u, v):
        """Agrega el arco u->v. Lanza ValueError si viola alguna restricción."""
        if u not in self.vertices or v not in self.vertices:
            raise ValueError("Vértice inexistente.")
        if u == v:
            raise ValueError("No se admiten lazos.")
        if (u, v) in self.arcos:
            raise ValueError("El arco ya existe (arco repetido).")
        if (v, u) in self.arcos:
            raise ValueError("Existe el arco recíproco %s->%s." % (v, u))
        self.arcos.append((u, v))

    def eliminar_arco(self, arco):
        """Elimina el arco indicado y cualquier estado de bloqueo asociado."""
        if arco not in self.arcos:
            raise ValueError("El arco no existe.")
        self.arcos.remove(arco)
        self.bloqueados.discard(arco)

    def alternar_bloqueo(self, arco):
        """Bloquea el arco si está activo; lo restablece si está bloqueado."""
        if arco in self.bloqueados:
            self.bloqueados.remove(arco)
        else:
            self.bloqueados.add(arco)

    def activos(self):
        """Devuelve la lista de arcos no bloqueados."""
        return [a for a in self.arcos if a not in self.bloqueados]


def camino_minimo_bfs(arcos, s, t):
    """Búsqueda en anchura desde s.
    Entrada: arcos (lista de (u,v)), s, t.
    Salida: lista de vértices [s,...,t] con el menor número de arcos, o None si no hay camino."""
    ady = {}
    for u, v in arcos:
        ady.setdefault(u, []).append(v)
    padre = {s: None}
    cola = deque([s])
    while cola:
        u = cola.popleft()
        if u == t:
            break
        for v in ady.get(u, []):
            if v not in padre:
                padre[v] = u
                cola.append(v)
    if t not in padre:
        return None
    camino = []
    v = t
    while v is not None:          # reconstrucción hacia atrás
        camino.append(v)
        v = padre[v]
    return camino[::-1]


def flujo_maximo(arcos, s, t):
    """Edmonds-Karp con capacidad 1 en cada arco.
    Salida: (valor del flujo, capacidades residuales finales)."""
    cap, ady = {}, {}
    for u, v in arcos:
        cap[(u, v)] = 1
        cap.setdefault((v, u), 0)     # arco inverso residual
        ady.setdefault(u, []).append(v)
        ady.setdefault(v, []).append(u)
    flujo = 0
    while True:
        padre = {s: None}
        cola = deque([s])
        while cola and t not in padre:
            u = cola.popleft()
            for v in ady.get(u, []):
                if v not in padre and cap[(u, v)] > 0:
                    padre[v] = u
                    cola.append(v)
        if t not in padre:
            return flujo, cap
        v = t
        while padre[v] is not None:   # aumenta 1 unidad por el camino hallado
            u = padre[v]
            cap[(u, v)] -= 1
            cap[(v, u)] += 1
            v = u
        flujo += 1


def caminos_sin_arcos_compartidos(arcos, s, t, flujo, cap):
    """Descompone el flujo en 'flujo' caminos de s a t sin arcos en común.
    Un arco (u,v) lleva flujo si su inverso residual (v,u) tiene capacidad 1."""
    sucesores = {}
    for u, v in arcos:
        if cap[(v, u)] == 1:
            sucesores.setdefault(u, []).append(v)
    caminos = []
    for _ in range(flujo):
        camino = [s]
        while camino[-1] != t:
            v = sucesores[camino[-1]].pop()
            if v in camino:           # descarta ciclos con flujo
                del camino[camino.index(v) + 1:]
            else:
                camino.append(v)
        caminos.append(camino)
    return caminos


def corte_minimo(arcos, s, cap):
    """Con el residual final: S = vértices alcanzables desde s.
    El corte son los arcos originales que salen de S hacia fuera de S."""
    ady = {}
    for (u, v), c in cap.items():
        if c > 0:
            ady.setdefault(u, []).append(v)
    S, cola = {s}, deque([s])
    while cola:
        u = cola.popleft()
        for v in ady.get(u, []):
            if v not in S:
                S.add(v)
                cola.append(v)
    return [(u, v) for (u, v) in arcos if u in S and v not in S]


def verificar(arcos, s, t, caminos, corte):
    """Comprobaciones del enunciado. Devuelve lista de (descripción, bool)."""
    conj = set(arcos)
    pares = [set(zip(c, c[1:])) for c in caminos]
    usados = [a for p in pares for a in p]
    return [
        ("Todos los caminos respetan los sentidos de arcos activos",
         all(c[0] == s and c[-1] == t and p <= conj for c, p in zip(caminos, pares))),
        ("Los caminos no comparten arcos", len(usados) == len(set(usados))),
        ("|corte| = número de caminos", len(corte) == len(caminos)),
        ("Al quitar el corte no hay camino de s a t",
         camino_minimo_bfs([a for a in arcos if a not in corte], s, t) is None),
    ]


def resolver(grafo, s, t):
    """Calcula todo para la configuración actual del grafo.
    Salida: dict con camino, distancia, k, caminos, corte y verificaciones."""
    arcos = grafo.activos()
    camino = camino_minimo_bfs(arcos, s, t)
    k, cap = flujo_maximo(arcos, s, t)
    caminos = caminos_sin_arcos_compartidos(arcos, s, t, k, cap)
    corte = corte_minimo(arcos, s, cap) if k > 0 else []   # sin camino: corte vacío
    return {"camino": camino,
            "distancia": None if camino is None else len(camino) - 1,
            "k": k, "caminos": caminos, "corte": corte,
            "verificacion": verificar(arcos, s, t, caminos, corte)}
