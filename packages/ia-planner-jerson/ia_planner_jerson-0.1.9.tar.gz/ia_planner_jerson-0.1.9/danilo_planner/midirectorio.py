from pathlib import Path
import os
import tkinter as tk
from tkinter import filedialog
import os

class MiClase:
    @staticmethod
    def select_directory():
        """Abre un cuadro de diálogo para que el usuario seleccione un directorio."""
        root = tk.Tk()
        root.withdraw() 
        directory = filedialog.askdirectory(title="Selecciona el directorio para guardar el planificador")
        
        if not directory:
            raise ValueError("No se seleccionó ningún directorio.")
        
        return os.path.normpath(directory)
    


