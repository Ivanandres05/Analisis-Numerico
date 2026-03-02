import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import matplotlib.cm as cm
import time
import math

import funciones.definiciones as fn
from metodos.biseccion import biseccion
from metodos.falsa_posicion import falsa_posicion
from metodos.punto_fijo import punto_fijo
from metodos.newton import newton_raphson
from metodos.secante import secante
import utils.validaciones as vl

def fmt_val(v):
    if v is None:
        return "-"
    if isinstance(v, float):
        if math.isinf(v) or math.isnan(v):
            return str(v)
        if v == 0.0:
            return "0.00000000"
        if abs(v) < 1e-4 or abs(v) > 1e4:
            return f"{v:.8e}"
        return f"{v:.8f}"
    return str(v)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos - Ingeniería de Software")
        self.geometry("1300x850")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # --- TOP FRAME ---
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        ttk.Label(self.top_frame, text="Seleccionar Ejercicio / Método:").pack(side=tk.LEFT, padx=5)
        self.combo_methods = ttk.Combobox(self.top_frame, width=60, state="readonly", values=[
            "1. Bisección (Optimización de Hash Table) [T(λ)]",
            "2. Falsa Posición (Balanceo de Carga) [E(x)]",
            "3. Punto Fijo (Crecimiento de BD) [x=g(x)]",
            "4. Newton-Raphson (Análisis de Concurrencia) [T(n)]",
            "5. Secante (Predicción de Escalabilidad) [P(x)]"
        ])
        self.combo_methods.pack(side=tk.LEFT, padx=5)
        self.combo_methods.bind("<<ComboboxSelected>>", self.on_method_change)
        
        # --- INPUT FRAME ---
        self.input_frame = ttk.LabelFrame(self, text="Parámetros de Entrada")
        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.input_container = ttk.Frame(self.input_frame)
        self.input_container.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # --- CONTENT FRAME ---
        self.content_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.content_paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 1. Table Frame
        self.left_panel = ttk.Frame(self.content_paned)
        self.content_paned.add(self.left_panel, weight=1)
        
        self.tree_frame = ttk.Frame(self.left_panel)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb = ttk.Scrollbar(self.left_panel, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.TOP, fill=tk.X)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.results_frame = ttk.LabelFrame(self.left_panel, text="Panel de Resultados Finales")
        self.results_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.lbl_result = ttk.Label(self.results_frame, text="", wraplength=450, foreground="purple", font=("TkDefaultFont", 10, "bold"))
        self.lbl_result.pack(padx=10, pady=10, fill=tk.X)
        
        # Secant vs Newton comparative table (for Ex 5 / Ex 2)
        self.comp_table = ttk.Treeview(self.results_frame, height=2, show="headings")
        # initially hidden
        
        # 2. Plot Frame
        self.plot_frame = ttk.Frame(self.content_paned)
        self.content_paned.add(self.plot_frame, weight=1)
        
        self.fig = Figure(figsize=(7, 8), dpi=100)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        
        # Inputs config
        self.inputs = {}
        
        self.combo_methods.current(0)
        self.on_method_change(None)

    def clear_inputs(self):
        for widget in self.input_container.winfo_children():
            widget.destroy()
        self.inputs.clear()
        
    def clear_table(self):
        self.tree.delete(*self.tree.get_children())
        
    def add_input(self, key, label, default_val, col, combobox_vals=None):
        ttk.Label(self.input_container, text=label).grid(row=0, column=col*2, padx=5, pady=5, sticky="e")
        var = tk.StringVar(value=default_val)
        if combobox_vals:
            wdg = ttk.Combobox(self.input_container, textvariable=var, values=combobox_vals, width=8)
        else:
            wdg = ttk.Entry(self.input_container, textvariable=var, width=10)
        wdg.grid(row=0, column=col*2+1, padx=5, pady=5, sticky="w")
        self.inputs[key] = var
        return wdg

    def add_buttons(self, col, calc_cmd, clear_cmd):
        ttk.Button(self.input_container, text="Calcular", command=calc_cmd).grid(row=0, column=col*2, padx=10)
        ttk.Button(self.input_container, text="Limpiar", command=clear_cmd).grid(row=0, column=col*2+1, padx=10)

    def configure_tree(self, columns):
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)

    def on_method_change(self, event):
        idx = self.combo_methods.current()
        self.clear_inputs()
        self.clear_table()
        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()
        self.lbl_result.config(text="")
        self.comp_table.pack_forget()
        
        if idx == 0:
            self.setup_bisection()
        elif idx == 1:
            self.setup_false_position()
        elif idx == 2:
            self.setup_fixed_point()
        elif idx == 3:
            self.setup_newton()
        elif idx == 4:
            self.setup_secant()

    # ==========================
    # EJERCICIO 1: BISECCIÓN
    # ==========================
    def setup_bisection(self):
        self.add_input("a", "a:", "0.5", 0)
        self.add_input("b", "b:", "2.5", 1)
        self.add_input("tol", "Tol:", "1e-6", 2)
        self.add_input("iter", "Max Iter:", "100", 3)
        self.add_buttons(4, self.calc_bisection, lambda: self.on_method_change(None))
        self.configure_tree(["Iteración (n)", "a", "b", "c", "f(c)", "Error Absoluto", "Error Relativo (%)"])
        
    def calc_bisection(self):
        try:
            a = vl.validar_numerico(self.inputs["a"].get(), "a")
            b = vl.validar_numerico(self.inputs["b"].get(), "b")
            tol = vl.validar_numerico(self.inputs["tol"].get(), "Tol")
            max_i = vl.validar_entero_positivo(self.inputs["iter"].get(), "Max Iter")
            
            self.clear_table()
            root, iters = biseccion(fn.f_bisection, a, b, tol, max_i)
            
            for it in iters:
                self.tree.insert("", tk.END, values=(
                    it['n'], fmt_val(it['a']), fmt_val(it['b']), fmt_val(it['c']), 
                    fmt_val(it['f(c)']), fmt_val(it['error_abs']), fmt_val(it['error_rel'])
                ))
            
            # Graficar
            self.ax1.clear()
            self.ax2.clear()
            
            x = np.linspace(a - 0.5, b + 0.5, 400)
            y = fn.f_bisection(x)
            self.ax1.plot(x, y, 'b-', label='T(λ)')
            self.ax1.axhline(0, color='black', lw=1)
            
            colors = cm.rainbow(np.linspace(0, 1, len(iters)))
            for i, it in enumerate(iters):
                self.ax1.scatter(it['c'], it['f(c)'], color=colors[i], zorder=5)
            self.ax1.scatter([root], [fn.f_bisection(root)], marker='*', s=150, color='lime', zorder=10, label='Raíz Final')
            
            self.ax1.set_title("Función y Convergencia de Aproximaciones")
            self.ax1.set_xlabel("λ (Factor de Carga)")
            self.ax1.set_ylabel("T(λ)")
            self.ax1.legend()
            
            self.ax2.plot([it['n'] for it in iters], [it['error_abs'] for it in iters], marker='o', linestyle='-', color='indigo')
            self.ax2.set_yscale('log')
            self.ax2.set_title("Convergencia del Error")
            self.ax2.set_xlabel("Iteración (n)")
            self.ax2.set_ylabel("Error Absoluto (log)")
            
            self.canvas.draw()
            
            self.lbl_result.config(text=f"¿Qué significa λ = {fmt_val(root)}?\n\nInterpretación: "
                                        "Es el factor de carga óptimo de la Hash Table que minimiza el tiempo "
                                        "promedio de búsqueda T(λ) y antes de generar colisiones excesivas.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # EJERCICIO 2: FALSA POSICIÓN
    # ==========================
    def setup_false_position(self):
        self.add_input("a", "a:", "2", 0)
        self.add_input("b", "b:", "4", 1)
        self.add_input("tol", "Tol:", "1e-7", 2)
        self.add_input("iter", "Max Iter:", "100", 3)
        self.add_input("metodo", "Método:", "Ambos", 4, ["Bisección", "Falsa Posición", "Ambos"])
        self.add_buttons(5, self.calc_false_pos, lambda: self.on_method_change(None))
        self.configure_tree(["Método", "Iter", "a", "b", "c", "f(c)", "Error Absoluto", "Error Relativo (%)"])
        
    def calc_false_pos(self):
        try:
            a = vl.validar_numerico(self.inputs["a"].get(), "a")
            b = vl.validar_numerico(self.inputs["b"].get(), "b")
            tol = vl.validar_numerico(self.inputs["tol"].get(), "Tol")
            max_i = vl.validar_entero_positivo(self.inputs["iter"].get(), "Max Iter")
            met = self.inputs["metodo"].get()
            
            self.clear_table()
            self.ax1.clear()
            self.ax2.clear()
            
            x = np.linspace(a - 0.5, b + 0.5, 400)
            y = fn.f_false_position(x)
            self.ax1.plot(x, y, 'blue', label='E(x)=x³-6x²+11x-6.5')
            self.ax1.axhline(0, color='black')
            
            msg = ""
            def put_table(meth_name, iters):
                for it in iters:
                    self.tree.insert("", tk.END, values=(
                        meth_name, it['n'], fmt_val(it['a']), fmt_val(it['b']), fmt_val(it['c']), 
                        fmt_val(it['f(c)']), fmt_val(it['error_abs']), fmt_val(it['error_rel'])
                    ))
                    
            if met in ["Bisección", "Ambos"]:
                st = time.perf_counter()
                r_b, it_b = biseccion(fn.f_false_position, a, b, tol, max_i)
                tm_b = (time.perf_counter() - st) * 1000
                put_table("Bisección", it_b)
                self.ax2.plot([i['n'] for i in it_b], [i['error_abs'] for i in it_b], 'o-', label='Bisección', color='orange')
                msg += f"Bisección: {len(it_b)} iteraciones | Tiempo: {tm_b:.3f} ms."
                
            if met in ["Falsa Posición", "Ambos"]:
                st = time.perf_counter()
                r_f, it_f = falsa_posicion(fn.f_false_position, a, b, tol, max_i)
                tm_f = (time.perf_counter() - st) * 1000
                put_table("Falsa Posición", it_f)
                self.ax2.plot([i['n'] for i in it_f], [i['error_abs'] for i in it_f], 's--', label='Falsa Posición', color='green')
                self.ax1.scatter([r_f], [fn.f_false_position(r_f)], marker='*', s=150, color='green', zorder=10, label='Raíz Final FP')
                msg += f"\nFalsa Posición: {len(it_f)} iteraciones | Tiempo: {tm_f:.3f} ms."
                
            self.ax1.set_title("Función de Eficiencia del Sistema")
            self.ax1.set_xlabel("x (Número de workers)")
            self.ax1.legend()
            
            self.ax2.set_yscale('log')
            self.ax2.set_title("Convergencia del Error: Falsa Posición vs Bisección")
            self.ax2.set_ylabel("Error Abs (log)")
            self.ax2.legend()
            
            self.canvas.draw()
            self.lbl_result.config(text="Análisis de Velocidad:\n" + msg + "\nEl método de Falsa Posición con la recta secante aproxima la raíz mucho más rápido visualmente, ahorrando recursos del balanceador.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # EJERCICIO 3: PUNTO FIJO
    # ==========================
    def setup_fixed_point(self):
        self.add_input("x0", "x0 inicial:", "1.0", 0, ["0.5", "1.0", "1.5", "2.0"])
        self.add_input("tol", "Tol:", "1e-8", 1)
        self.add_input("iter", "Max Iter:", "100", 2)
        ttk.Button(self.input_container, text="Calcular", command=lambda: self.calc_fixed_point(False)).grid(row=0, column=6, padx=5)
        ttk.Button(self.input_container, text="Probar Todos", command=lambda: self.calc_fixed_point(True)).grid(row=0, column=7, padx=5)
        ttk.Button(self.input_container, text="Limpiar", command=lambda: self.on_method_change(None)).grid(row=0, column=8, padx=5)
        
        self.configure_tree(["x0 (Input)", "Iter (n)", "x_n", "g(x_n)", "|x_n - g(x_n)|", "Error Relativo (%)"])

    def calc_fixed_point(self, all_x0):
        try:
            tol = vl.validar_numerico(self.inputs["tol"].get(), "Tol")
            max_i = vl.validar_entero_positivo(self.inputs["iter"].get(), "Max Iter")
            
            self.clear_table()
            self.ax1.clear()
            self.ax2.clear()
            
            # Base logic
            x = np.linspace(0, 2.5, 400)
            self.ax1.plot(x, x, 'k--', label='y = x')
            self.ax1.plot(x, fn.g_fixed_point(x), 'b-', label='y = g(x) = 0.5cos(x)+1.5')
            
            targets = [0.5, 1.0, 1.5, 2.0] if all_x0 else [float(self.inputs["x0"].get())]
            colors = ['red', 'green', 'magenta', 'orange']
            
            first_root = -1
            for idx, x_0 in enumerate(targets):
                c = colors[idx % len(colors)]
                dg_val = abs(fn.dg_fixed_point(x_0))
                
                try:
                    root, iters = punto_fijo(fn.g_fixed_point, x_0, tol, max_i)
                    if first_root == -1: first_root = root
                    
                    for it in iters:
                        self.tree.insert("", tk.END, values=(
                            x_0, it['n'], fmt_val(it['x_n']), fmt_val(it['g(x_n)']), 
                            fmt_val(it['error_abs']), fmt_val(it['error_rel'])
                        ))
                    
                    self.ax2.plot([i['n'] for i in iters], [i['error_abs'] for i in iters], 
                                  linestyle='-', marker='.', color=c, label=f"x0={x_0} (|g'(x0)|={dg_val:.2f})")
                                  
                    # Cobweb
                    cx, cy = [x_0], [0]
                    for it in iters:
                        xn, gxn = it['x_n'], it['g(x_n)']
                        cx.append(xn); cy.append(gxn)
                        cx.append(gxn); cy.append(gxn)
                    self.ax1.plot(cx, cy, color=c, linewidth=1, alpha=0.7)
                    self.ax1.scatter([root], [root], color=c, marker='*', s=150, zorder=10)
                        
                except Exception as e:
                    self.ax2.plot([], [], label=f"x0={x_0} Divergió", color=c)
            
            self.ax1.set_title("Diagrama de Telaraña (Cobweb Plot)")
            self.ax1.legend()
            self.ax2.set_yscale('log')
            self.ax2.set_title("Convergencia según Valor Inicial")
            self.ax2.legend()
            self.canvas.draw()
            
            self.lbl_result.config(text=f"Mes de desborde de DB: ~{fmt_val(first_root)} meses.\n\n"
                            "Análisis: El método converge porque |g'(x)| < 1 en el dominio. "
                            "Un x0 más cercano a la raíz real exige menos iteraciones. "
                            "El Cobweb plot demuestra cómo el sistema espirala hacia el equilibrio.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # EJERCICIO 4: NEWTON-RAPHSON
    # ==========================
    def setup_newton(self):
        self.add_input("n0", "n0 (Threads):", "3.0", 0, ["1.0", "2.0", "3.0", "5.0"])
        self.add_input("tol", "Tol:", "1e-10", 1)
        self.add_input("iter", "Max Iter:", "100", 2)
        ttk.Button(self.input_container, text="Calcular", command=lambda: self.calc_newton(False)).grid(row=0, column=6, padx=5)
        ttk.Button(self.input_container, text="Probar Todos", command=lambda: self.calc_newton(True)).grid(row=0, column=7, padx=5)
        ttk.Button(self.input_container, text="Limpiar", command=lambda: self.on_method_change(None)).grid(row=0, column=8, padx=5)
        
        self.configure_tree(["Iter", "x_n (n0 input)", "f(x_n)", "f'(x_n)", "Error Absoluto", "Error Relativo (%)"])

    def calc_newton(self, all_n0):
        try:
            tol = vl.validar_numerico(self.inputs["tol"].get(), "Tol")
            max_i = vl.validar_entero_positivo(self.inputs["iter"].get(), "Max Iter")
            
            self.clear_table()
            self.ax1.clear()
            self.ax2.clear()
            
            x = np.linspace(0, 6, 400)
            self.ax1.plot(x, fn.f_newton(x), 'b-', label="T(n)=n³-8n²+20n-16")
            self.ax1.axhline(0, color='black')
            
            targets = [1.0, 2.0, 3.0, 5.0] if all_n0 else [float(self.inputs["n0"].get())]
            colors = ['red', 'green', 'magenta', 'orange']
            
            fin_root = None
            for idx, nx in enumerate(targets):
                c = colors[idx]
                root, iters = newton_raphson(fn.f_newton, fn.df_newton, nx, tol, max_i)
                if fin_root is None: fin_root = root
                
                for i, it in enumerate(iters):
                    self.tree.insert("", tk.END, values=(
                        it['n'], f"{fmt_val(it['x_n'])} (n0={nx})", fmt_val(it['f(x_n)']), 
                        fmt_val(it["f'(x_n)"]), fmt_val(it['error_abs']), fmt_val(it['error_rel'])
                    ))
                    # Plot tangents for the specific selected one or the first of all
                    if i < 4 and not all_n0:
                        tnx = it['x_n']
                        tf = it['f(x_n)']
                        tdf = it["f'(x_n)"]
                        tx = np.linspace(tnx - 1, tnx + 1, 50)
                        ty = tdf * (tx - tnx) + tf
                        self.ax1.plot(tx, ty, '--', color=c, alpha=0.5)
                        self.ax1.scatter([tnx], [tf], color=c)

                self.ax2.plot([it['n'] for it in iters], [it['error_abs'] for it in iters], marker='s', label=f'n0={nx}', color=c)
                self.ax1.scatter([root], [0], marker='*', s=150, zorder=10, color=c)
                
            self.ax1.legend()
            self.ax1.set_title("Tangentes de Newton-Raphson")
            self.ax2.legend()
            self.ax2.set_title("Convergencia Cuadrática (Observar caída brusca logarítmica)")
            self.ax2.set_yscale('log')
            self.canvas.draw()
            
            self.lbl_result.config(text=f"Número óptimo de Threads balanceado: {fmt_val(fin_root)}.\n\n"
                    "Convergencia: El error decae en patrón cuadrático E_(n+1) < (E_n)², "
                    "proporcionando una veloz aproximación al punto cŕitico concurrente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # EJERCICIO 5: SECANTE Y COMPARATIVA FINAL
    # ==========================
    def setup_secant(self):
        self.add_input("x0", "x0:", "0.5", 0)
        self.add_input("x1", "x1:", "1.0", 1)
        self.add_input("tol", "Tol:", "1e-9", 2)
        self.add_input("iter", "Max Iter:", "100", 3)
        self.add_buttons(4, self.calc_secant, lambda: self.on_method_change(None))
        self.configure_tree(["Iter (n)", "x_{n-1}", "x_n", "f(x_{n-1})", "f(x_n)", "x_{n+1}", "Error Absoluto"])
        
        self.comp_table.pack(fill=tk.X, padx=10, pady=5)
        self.comp_table["columns"] = ("Metodo", "Iteraciones", "Eval_Funcion", "Tiempo_ms", "Raiz")
        for col in self.comp_table["columns"]:
            self.comp_table.heading(col, text=col)
            self.comp_table.column(col, width=120, anchor=tk.CENTER)

    def calc_secant(self):
        try:
            x0 = vl.validar_numerico(self.inputs["x0"].get(), "x0")
            x1 = vl.validar_numerico(self.inputs["x1"].get(), "x1")
            tol = vl.validar_numerico(self.inputs["tol"].get(), "Tol")
            max_i = vl.validar_entero_positivo(self.inputs["iter"].get(), "Max Iter")
            
            self.clear_table()
            self.comp_table.delete(*self.comp_table.get_children())
            self.ax1.clear()
            self.ax2.clear()
            
            # Secant exec
            st = time.perf_counter()
            r_s, it_s = secante(fn.f_secant, x0, x1, tol, max_i)
            tm_s = (time.perf_counter() - st) * 1000
            
            # Newton exec on same function to compare (Uses x1 as start point)
            st_n = time.perf_counter()
            r_n, it_n = newton_raphson(fn.f_secant, fn.df_secant_for_newton, x1, tol, max_i)
            tm_n = (time.perf_counter() - st_n) * 1000
            
            # Populate Comparative
            self.comp_table.insert("", tk.END, values=("Secante", len(it_s), len(it_s)+2, fmt_val(tm_s), fmt_val(r_s)))
            self.comp_table.insert("", tk.END, values=("Newton-Raphson", len(it_n), len(it_n)*2, fmt_val(tm_n), fmt_val(r_n)))
            
            # Detail table Secant
            for it in it_s:
                self.tree.insert("", tk.END, values=(
                    it['n'], fmt_val(it['x_{n-1}']), fmt_val(it['x_n']), fmt_val(it['f(x_{n-1})']), 
                    fmt_val(it['f(x_n)']), fmt_val(it['x_{n+1}']), fmt_val(it['error_abs'])
                ))
            
            # Plot
            x = np.linspace(0.2, 2.5, 400)
            self.ax1.plot(x, fn.f_secant(x), 'blue', label='P(x) = x e^{-x/2} - 0.3')
            self.ax1.axhline(0, color='black')
            
            for i, it in enumerate(it_s[:4]): 
                px, cx = it['x_{n-1}'], it['x_n']
                py, cy = it['f(x_{n-1})'], it['f(x_n)']
                self.ax1.plot([px, cx], [py, cy], 'r--', alpha=0.6)
                self.ax1.scatter([px, cx], [py, cy], color='red')
            
            self.ax1.scatter([r_s], [0], color='green', marker='*', s=150, zorder=10, label='Cruce a Cero')
            self.ax1.legend()
            self.ax1.set_title("Aproximación por Rectas Secantes")
            
            self.ax2.plot([i['n'] for i in it_s], [i['error_abs'] for i in it_s], 'o-', label='Secante', color='red')
            self.ax2.plot([i['n'] for i in it_n], [i['error_abs'] for i in it_n], 's--', label='Newton-R', color='blue')
            self.ax2.set_yscale('log')
            self.ax2.set_title("Comparativa del Error Absoluto")
            self.ax2.legend()
            
            self.canvas.draw()
            self.lbl_result.config(text=f"Ingresos vs Costos Cloud equilibrados en {fmt_val(r_s)} miles de usuarios.\n\n"
                    "Análisis comparativo: El método de la de la Secante ahorra evaluaciones al no "
                    "requerir cálculos de derivadas (muy valioso en funciones costosas o complejas analíticamente "
                    "como esta exponencial), haciéndolo computacionalmente competitivo frente a Newton-Raphson.")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
