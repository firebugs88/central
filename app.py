import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
import threading
import atexit
import openpyxl
from concurrent.futures import ThreadPoolExecutor
import logging
from queue import Queue
from typing import Optional
import contextlib

@contextlib.contextmanager
def get_cursor(self):
    cursor  = self.conn.cursor()
    try:
        yield cursor
        self.conn.commit()
    except Exception as e:
        self.conn.rollback()
        raise e

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='novedades.log'
)

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()
    _connection_pool = Queue(maxsize=5)

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        for _ in range(5):
            conn = sqlite3.connect("pro.db", check_same_thread=False)
            self._connection_pool.put(conn)
        self._create_tables()

    def _create_tables(self):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS novedades (
                        id INTEGER PRIMARY KEY,
                        novedad TEXT NOT NULL,
                        fecha_inicio TEXT NOT NULL,
                        fecha_fin TEXT
                    )''')

    @contextlib.contextmanager
    def get_connection(self):
        connection = self._connection_pool.get()
        try:
            yield connection
        finally:
            self._connection_pool.put(connection)

    def close_all(self):
        while not self._connection_pool.empty():
            conn = self._connection_pool.get()
            conn.close()

class NovedadesRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def agregar_novedad(self, novedad: str, fecha_inicio: str) -> bool:
        try:
            with self.db.get_connection() as conn:
                c = conn.cursor()
                c.execute("INSERT INTO novedades (novedad, fecha_inicio) VALUES (?, ?)", 
                         (novedad, fecha_inicio))
                conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error al agregar novedad: {e}")
            return False

    def obtener_novedades(self):
        with self.db.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM novedades")
            return c.fetchall()

    def actualizar_novedad(self, novedad_id: int, nueva_novedad: str) -> bool:
        try:
            with self.db.get_connection() as conn:
                c = conn.cursor()
                c.execute("UPDATE novedades SET novedad = ? WHERE id = ?",
                         (nueva_novedad, novedad_id))
                conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error al actualizar novedad: {e}")
            return False

    def eliminar_novedad(self, novedad_id: int) -> bool:
        try:
            with self.db.get_connection() as conn:
                c = conn.cursor()
                c.execute("DELETE FROM novedades WHERE id = ?", (novedad_id,))
                conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error al eliminar novedad: {e}")
            return False

    def terminar_novedad(self, novedad_id: int, fecha_fin: str) -> bool:
        try:
            with self.db.get_connection() as conn:
                c = conn.cursor()
                c.execute("UPDATE novedades SET fecha_fin = ? WHERE id = ?",
                         (fecha_fin, novedad_id))
                conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error al terminar novedad: {e}")
            return False

class NovedadesGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.repository = NovedadesRepository()
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.setup_ui()
        self._setup_styles()

    def _setup_styles(self):
        style = ttk.Style()
        style.configure("Custom.Treeview",
                       background="#ffffff",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="#ffffff")
        style.map('Custom.Treeview',
                 background=[('selected', '#0078D7')])

    def setup_ui(self):
        self.root.title("Registro de Novedades Diarias")
        self.root.configure(bg="#c2eaec")
        self.root.geometry("800x600")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.frame = tk.Frame(self.root, bg="#c2eaec", padx=20, pady=20)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.entrada_novedad = tk.Entry(self.frame, width=50)
        self.entrada_novedad.grid(row=0, column=0, columnspan=4, pady=10)
        self.entrada_novedad.bind("<Return>", self.agregar_novedad)

        self._setup_buttons()
        self._setup_treeview()
        self.contador_novedades_sin_terminar = tk.StringVar()
        self._setup_contador()

    def _setup_buttons(self):
        buttons = [
            ("Crear", self.agregar_novedad, "#aed581"),
            ("Terminar", self.terminar_novedad, "#c8e6c9"),
            ("Editar", self.editar_novedad, "#fff9c4"),
            ("Eliminar", self.eliminar_novedad, "#e57373"),
            ("Exportar", self.exportar_novedad, "#76b5c5")
        ]

        for i, (text, command, color) in enumerate(buttons):
            tk.Button(self.frame, text=text, command=command, bg=color, fg="black")\
                .grid(row=1, column=i, padx=5, pady=5)

    def _setup_treeview(self):
        columns = ("ID", "Novedad", "Fecha de Inicio", "Fecha de Fin")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings",
                                style="Custom.Treeview")
        
        # Configurar las cabeceras
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
        
        # Configurar las columnas con pesos para el redimensionamiento
        self.tree.column("ID", width=30, anchor="center", minwidth=20, stretch=False)
        self.tree.column("Novedad", width=300, minwidth=200, stretch=True)
        self.tree.column("Fecha de Inicio", width=150, minwidth=150, stretch=False, anchor="center")
        self.tree.column("Fecha de Fin", width=150, minwidth=150, stretch=False, anchor="center")

        # Configurar el grid con peso para que se expanda
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.tree.tag_configure("sin_fecha_fin", background="#e5a8c5")

        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

    def _setup_contador(self):
        label_contador = tk.Label(
            self.frame,
            textvariable=self.contador_novedades_sin_terminar,
            bg="#e6e6e6",
            fg="#ea76e4",
            font=("Arial", 14, "bold")
        )
        label_contador.grid(row=2, column=0, columnspan=5, pady=10)

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        rows = self.repository.obtener_novedades()
        contador = 0
        
        for row in rows:
            fecha_inicio = self._format_date(row[2])
            fecha_fin = self._format_date(row[3]) if row[3] else "Pendiente"
            
            self.tree.insert("", "end",
                            values=(row[0], row[1], fecha_inicio, fecha_fin),
                            tags=("sin_fecha_fin",) if row[3] is None else ())
            
            if row[3] is None:
                contador += 1
        
        self.contador_novedades_sin_terminar.set(f"Novedades sin terminar: {contador}")

    @staticmethod
    def _format_date(date_str: Optional[str]) -> str:
        if not date_str:
            return ""
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y, %I:%M:%S %p")

    def agregar_novedad(self, event=None):
        novedad = self.entrada_novedad.get().strip()
        if not novedad:
            messagebox.showwarning("Advertencia", "El campo de novedad no puede estar vacío.")
            return
        
        if len(novedad) > 255:
            messagebox.showwarning("Advertencia", "La Novedad Es Demasiado Larga.")
            return

        fecha_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        def _agregar():
            if self.repository.agregar_novedad(novedad, fecha_inicio):
                self.root.after(0, self.actualizar_lista)
                self.root.after(0, lambda: self.entrada_novedad.delete(0, tk.END))
            else:
                messagebox.showerror("Error", "No se pudo agregar la novedad")
        
        self.executor.submit(_agregar)

    def editar_novedad(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una novedad para editar.")
            return

        item = self.tree.item(selected_item)
        novedad_id = item['values'][0]
        nueva_novedad = self.entrada_novedad.get()
        
        def _editar():
            if self.repository.actualizar_novedad(novedad_id, nueva_novedad):
                self.root.after(0, self.actualizar_lista)
            else:
                messagebox.showerror("Error", "No se pudo editar la novedad")
        
        self.executor.submit(_editar)

    def eliminar_novedad(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una novedad para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta novedad?"):
            item = self.tree.item(selected_item)
            novedad_id = item['values'][0]
            
            def _eliminar():
                if self.repository.eliminar_novedad(novedad_id):
                    self.root.after(0, self.actualizar_lista)
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la novedad")
            
            self.executor.submit(_eliminar)

    def terminar_novedad(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una novedad para marcar como terminada.")
            return

        item = self.tree.item(selected_item)
        novedad_id = item['values'][0]
        fecha_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        def _terminar():
            if self.repository.terminar_novedad(novedad_id, fecha_fin):
                self.root.after(0, self.actualizar_lista)
            else:
                messagebox.showerror("Error", "No se pudo terminar la novedad")
        
        self.executor.submit(_terminar)

    def exportar_novedad(self):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Novedades"
        
        # Encabezados
        worksheet.append(["ID", "Novedad", "Fecha Inicio", "Fecha Fin"])
        
        # Datos
        rows = self.repository.obtener_novedades()
        for row in rows:
            fecha_inicio = self._format_date(row[2])
            fecha_fin = self._format_date(row[3]) if row[3] else "Pendiente"
            worksheet.append([row[0], row[1], fecha_inicio, fecha_fin])

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if file_path:
            try:
                workbook.save(file_path)
                messagebox.showinfo("Exportado", f"Las novedades se han exportado correctamente a {file_path}.")
            except Exception as e:
                logging.error(f"Error al exportar: {e}")
                messagebox.showerror("Error", "No se pudo exportar el archivo")
        else:
            messagebox.showinfo("Cancelado", "Exportación cancelada por el usuario.")

    def run(self):
        self.actualizar_lista()
        self.root.mainloop()

if __name__ == "__main__":
    app = NovedadesGUI()
    app.run()