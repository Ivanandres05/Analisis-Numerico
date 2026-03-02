import sys
import os

# Asegurar que el entorno local esté en el path (útil si se corre desde diferentes ubicaciones)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from interfaz.gui_principal import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
