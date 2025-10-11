import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow

from ..generated.Ui_main_window import Ui_MainWindow

class FinancialTerminalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """Inicializa la configuración de la interfaz de usuario."""
        self.setWindowTitle("FinCore Terminal")
        
        # Cargar hoja de estilos de forma robusta
        script_dir = os.path.dirname(os.path.abspath(__file__))
        style_sheet_path = os.path.join(script_dir, "..", "..", "assets", "styles", "style.qss")
        self.load_style_sheet(style_sheet_path)
    
    def _connect_signals(self):
        """Conecta las señales de los widgets a los slots."""
        # Ejemplo: Conectar un cambio en el campo de búsqueda a una función
        # self.ui.searchLineEdit.textChanged.connect(self.on_search_text_changed)
        pass

    def load_style_sheet(self, path):
        """
        Carga una hoja de estilo QSS desde un archivo y la aplica a la aplicación.
        """
        try:
            with open(path, "r") as f:
                style_sheet = f.read()
                self.setStyleSheet(style_sheet)
                print(f"Hoja de estilo cargada exitosamente desde: {path}")
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo de estilos en '{path}'.")
        except Exception as e:
            print(f"Ocurrió un error al cargar los estilos: {e}")




