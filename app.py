"""
Simulador interactivo de laberintos y rutas alternativas (INFO1158).
Interfaz con tkinter (biblioteca estándar). Ejecutar: python app.py
"""
import math
import tkinter as tk
from tkinter import ttk, messagebox
from algoritmos import Grafo, resolver
from datos import POS, ARCOS

COLORES = ["#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf", "#8c564b"]
R = 18  # radio de los vértices


class App:
    def __init__(self, root):
        root.title("Simulador de laberintos y rutas alternativas")
        self.g = Grafo(POS.keys(), ARCOS)
        self.s, self.t, self.sel, self.res = "s", "t", None, None
        self._estado_inicial = self._estado_actual()
        self._historial = [self._estado_inicial]
        self._pos_historial = 0
        self.configuraciones = {"Original": self._estado_inicial}
        self.cv = tk.Canvas(root, width=800, height=500, bg="white")
        self.cv.grid(row=0, column=0, padx=5, pady=5)
        self.cv.bind("<Button-1>", self.click)
        p = ttk.Frame(root)
        p.grid(row=0, column=1, sticky="n", padx=5, pady=5)

        self.vista = tk.StringVar(value="min")
        ttk.Label(p, text="Resaltar:").pack(anchor="w")
        for txt, val in [("Camino mínimo", "min"), ("Caminos sin arcos compartidos", "disj"),
                         ("Corte mínimo", "corte"), ("Ninguno", "no")]:
            ttk.Radiobutton(p, text=txt, value=val, variable=self.vista,
                            command=self.dibujar).pack(anchor="w")

        ttk.Label(p, text="\nEntrada / Salida:").pack(anchor="w")
        f = ttk.Frame(p); f.pack(anchor="w")
        self.cs = ttk.Combobox(f, values=list(POS), width=3, state="readonly")
        self.ct = ttk.Combobox(f, values=list(POS), width=3, state="readonly")
        self.cs.set("s"); self.ct.set("t")
        self.cs.pack(side="left"); self.ct.pack(side="left", padx=4)
        ttk.Button(f, text="Aplicar", command=self.cambiar_st).pack(side="left")

        ttk.Label(p, text="\nPasillo seleccionado (clic en un arco):").pack(anchor="w")
        self.lsel = ttk.Label(p, text="ninguno"); self.lsel.pack(anchor="w")
        ttk.Button(p, text="Bloquear / Restablecer", command=self.bloquear).pack(anchor="w")
        ttk.Button(p, text="Eliminar pasillo", command=self.eliminar).pack(anchor="w")

        f_hist = ttk.Frame(p); f_hist.pack(anchor="w", pady=4)
        ttk.Button(f_hist, text="Deshacer", command=self.deshacer).pack(side="left")
        ttk.Button(f_hist, text="Rehacer", command=self.rehacer).pack(side="left", padx=4)
        ttk.Button(p, text="Restablecer grafo original", command=self.restablecer_original).pack(anchor="w")

        ttk.Label(p, text="\nConfiguraciones para comparar:").pack(anchor="w")
        f_config = ttk.Frame(p); f_config.pack(anchor="w")
        self.config_sel = ttk.Combobox(
            f_config, values=["Original", "Modificación 1", "Modificación 2"],
            width=16, state="readonly")
        self.config_sel.set("Modificación 1")
        self.config_sel.pack(side="left")
        ttk.Button(f_config, text="Guardar actual", command=self.guardar_configuracion).pack(
            side="left", padx=4)
        ttk.Button(p, text="Comparar configuraciones", command=self.comparar_configuraciones).pack(
            anchor="w", pady=2)

        ttk.Label(p, text="\nAgregar pasillo u -> v:").pack(anchor="w")
        f2 = ttk.Frame(p); f2.pack(anchor="w")
        self.cu = ttk.Combobox(f2, values=list(POS), width=3, state="readonly")
        self.cv2 = ttk.Combobox(f2, values=list(POS), width=3, state="readonly")
        self.cu.pack(side="left"); self.cv2.pack(side="left", padx=4)
        ttk.Button(f2, text="Agregar", command=self.agregar).pack(side="left")

        ttk.Button(p, text="\nRecalcular", command=self.recalcular).pack(anchor="w", pady=8)
        self.txt = tk.Text(p, width=44, height=22, font=("Consolas", 9))
        self.txt.pack()
        self.recalcular()

    def _estado_actual(self):
        """Devuelve una copia del estado editable actual de la aplicación."""
        return (list(self.g.arcos), set(self.g.bloqueados), self.s, self.t)

    def _registrar_estado(self):
        """Guarda el estado actual y descarta la rama posterior si hubo un deshacer."""
        estado = self._estado_actual()
        if estado == self._historial[self._pos_historial]:
            return
        self._historial = self._historial[:self._pos_historial + 1]
        self._historial.append(estado)
        self._pos_historial += 1

    def _restaurar_estado(self, estado):
        """Restaura un estado guardado en el historial."""
        arcos, bloqueados, self.s, self.t = estado
        self.g.arcos = list(arcos)
        self.g.bloqueados = set(bloqueados)
        self.sel = None
        self.lsel.config(text="ninguno")
        self.cs.set(self.s)
        self.ct.set(self.t)
        self.recalcular()

    def recalcular(self):
        """Ejecuta los algoritmos sobre la configuración actual y actualiza pantalla."""
        self.res = resolver(self.g, self.s, self.t)
        r = self.res
        L = ["Entrada: %s   Salida: %s" % (self.s, self.t),
             "Arcos activos: %d (bloqueados: %d)" % (len(self.g.activos()), len(self.g.bloqueados))]
        if r["camino"] is None:
            L.append("\nNo existe camino de s a t.")
        else:
            L.append("\nCamino mínimo (%d arcos):\n  %s" % (r["distancia"], " -> ".join(r["camino"])))
        L.append("\nMáx. caminos sin arcos compartidos: %d" % r["k"])
        for i, c in enumerate(r["caminos"], 1):
            L.append("  %d) %s" % (i, " -> ".join(c)))
        L.append("\nCorte mínimo (%d arcos): %s" % (len(r["corte"]),
                 ", ".join("%s->%s" % a for a in r["corte"]) or "conjunto vacío"))
        L.append("\nVerificaciones:")
        for d, ok in r["verificacion"]:
            L.append("  [%s] %s" % ("OK" if ok else "FALLA", d))
        self.txt.delete("1.0", "end"); self.txt.insert("end", "\n".join(L))
        self.dibujar()

    def extremos(self, a):
        """Puntos de inicio/fin de un arco, recortados al borde de los círculos."""
        (x1, y1), (x2, y2) = POS[a[0]], POS[a[1]]
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        return x1 + ux * R, y1 + uy * R, x2 - ux * R, y2 - uy * R

    def dibujar(self):
        self.cv.delete("all")
        r, v = self.res, self.vista.get()
        resalte = {}   # arco -> color
        if r and v == "min" and r["camino"]:
            resalte = {a: COLORES[0] for a in zip(r["camino"], r["camino"][1:])}
        elif r and v == "disj":
            for i, c in enumerate(r["caminos"]):
                for a in zip(c, c[1:]):
                    resalte[a] = COLORES[i % len(COLORES)]
        elif r and v == "corte":
            resalte = {a: "red" for a in r["corte"]}
        for a in self.g.arcos:
            x1, y1, x2, y2 = self.extremos(a)
            if a == self.sel:
                self.cv.create_line(x1, y1, x2, y2, width=10, fill="#ffe0a3")
            if a in self.g.bloqueados:
                self.cv.create_line(x1, y1, x2, y2, fill="gray", dash=(4, 4), arrow=tk.LAST)
            elif a in resalte:
                self.cv.create_line(x1, y1, x2, y2, fill=resalte[a], width=4,
                                    arrow=tk.LAST, arrowshape=(14, 16, 6))
            else:
                self.cv.create_line(x1, y1, x2, y2, fill="black", arrow=tk.LAST)
        for n, (x, y) in POS.items():
            col = "#b7e4c7" if n == self.s else "#ffe08a" if n == self.t else "#eeeeee"
            self.cv.create_oval(x - R, y - R, x + R, y + R, fill=col, outline="black")
            self.cv.create_text(x, y, text=n, font=("Arial", 11, "bold"))

    def click(self, e):
        """Selecciona el arco más cercano al clic (a menos de 10 px)."""
        mejor, dmin = None, 10
        for a in self.g.arcos:
            x1, y1, x2, y2 = self.extremos(a)
            dx, dy = x2 - x1, y2 - y1
            u = max(0, min(1, ((e.x - x1) * dx + (e.y - y1) * dy) / (dx * dx + dy * dy)))
            d = math.hypot(e.x - (x1 + u * dx), e.y - (y1 + u * dy))
            if d < dmin:
                mejor, dmin = a, d
        self.sel = mejor
        self.lsel.config(text="%s -> %s" % mejor if mejor else "ninguno")
        self.dibujar()

    def bloquear(self):
        if self.sel:
            self.g.alternar_bloqueo(self.sel)
            self._registrar_estado()
            self.recalcular()

    def eliminar(self):
        """Elimina el arco seleccionado y actualiza la visualización."""
        if not self.sel:
            messagebox.showwarning("Sin selección", "Selecciona un pasillo para eliminarlo.")
            return
        arco = self.sel
        try:
            self.g.eliminar_arco(arco)
        except ValueError as ex:
            messagebox.showerror("Pasillo no válido", str(ex))
            return
        self.sel = None
        self.lsel.config(text="ninguno")
        self._registrar_estado()
        self.recalcular()

    def agregar(self):
        try:
            self.g.agregar_arco(self.cu.get(), self.cv2.get())
        except ValueError as ex:
            messagebox.showerror("Pasillo no válido", str(ex)); return
        self._registrar_estado()
        self.recalcular()

    def cambiar_st(self):
        if self.cs.get() == self.ct.get():
            messagebox.showerror("Error", "Entrada y salida deben ser distintas."); return
        self.s, self.t = self.cs.get(), self.ct.get()
        self._registrar_estado()
        self.recalcular()

    def deshacer(self):
        """Vuelve al estado anterior del historial."""
        if self._pos_historial == 0:
            return
        self._pos_historial -= 1
        self._restaurar_estado(self._historial[self._pos_historial])

    def rehacer(self):
        """Avanza al siguiente estado disponible del historial."""
        if self._pos_historial >= len(self._historial) - 1:
            return
        self._pos_historial += 1
        self._restaurar_estado(self._historial[self._pos_historial])

    def restablecer_original(self):
        """Restaura el grafo, la entrada y la salida de la configuración inicial."""
        self._restaurar_estado(self._estado_inicial)
        self._registrar_estado()
        self.recalcular()

    def guardar_configuracion(self):
        """Guarda el estado actual con el nombre seleccionado para compararlo después."""
        nombre = self.config_sel.get()
        if not nombre:
            messagebox.showwarning("Configuración", "Selecciona el nombre de la configuración.")
            return
        _, _, s, t = self._estado_actual()
        _, _, s_inicial, t_inicial = self._estado_inicial
        if (s, t) != (s_inicial, t_inicial):
            messagebox.showwarning(
                "Extremos distintos",
                "Para comparar configuraciones debes mantener s=%s y t=%s."
                % (s_inicial, t_inicial))
            return
        self.configuraciones[nombre] = self._estado_actual()
        messagebox.showinfo("Configuración guardada", "%s quedó guardada." % nombre)

    def comparar_configuraciones(self):
        """Muestra los resultados de las configuraciones guardadas."""
        nombres = ["Original", "Modificación 1", "Modificación 2"]
        faltantes = [n for n in nombres if n not in self.configuraciones]
        if faltantes:
            messagebox.showwarning(
                "Configuraciones incompletas",
                "Guarda primero: %s." % ", ".join(faltantes))
            return

        lineas = ["Comparación de configuraciones\n"]
        for nombre in nombres:
            arcos, bloqueados, s, t = self.configuraciones[nombre]
            grafo = Grafo(POS.keys(), arcos)
            grafo.bloqueados = set(bloqueados)
            resultado = resolver(grafo, s, t)
            camino = " -> ".join(resultado["camino"]) if resultado["camino"] else "No existe"
            corte = ", ".join("%s->%s" % arco for arco in resultado["corte"]) or "conjunto vacío"
            lineas.extend([
                "%s (%s -> %s)" % (nombre, s, t),
                "  Camino mínimo: %s" % camino,
                "  Longitud: %s" % (resultado["distancia"]
                                     if resultado["distancia"] is not None else "no aplica"),
                "  Caminos sin arcos compartidos: %d" % resultado["k"],
                "  Corte mínimo (%d): %s\n" % (len(resultado["corte"]), corte),
            ])
        messagebox.showinfo("Comparación", "\n".join(lineas))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
