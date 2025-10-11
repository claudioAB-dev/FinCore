import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow

# Importa el gestor de la base de datos
from ...core.database import DatabaseManager 
from ..generated.Ui_main_window import Ui_MainWindow

class FinancialTerminalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 1. Inicializar el gestor de la base de datos
        self.db = DatabaseManager()

        self._init_ui()
        self._connect_signals()
        
        # 2. Cargar datos iniciales (opcional)
        self.load_portfolio_data()

    def _init_ui(self):
        """Inicializa la configuración de la interfaz de usuario."""
        self.setWindowTitle("FinCore Terminal")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        style_sheet_path = os.path.join(script_dir, "..", "..", "assets", "styles", "styles.qss")
        self.load_style_sheet(style_sheet_path)
    
    def _connect_signals(self):
        """Conecta las señales de los widgets a los slots."""
        # Aquí podrías conectar botones para añadir o eliminar acciones
        # self.ui.addButton.clicked.connect(self.add_new_stock)
        pass

    def load_portfolio_data(self):
        """
        Carga los datos del portfolio desde la DB y los muestra en la UI.
        """
        stocks = self.db.get_all_stocks()
        print("Datos del portfolio cargados:")
        for stock in stocks:
            print(stock)

    def load_style_sheet(self, path):
        """
        Carga una hoja de estilo QSS desde un archivo y la aplica a la aplicación.
        """
        try:
            with open(path, "r") as f:
                style_sheet = f.read()
                self.setStyleSheet(style_sheet)
        except Exception as e:
            print(f"Ocurrió un error al cargar los estilos: {e}")
            
    def closeEvent(self, event):
        """
        Asegura que la conexión a la base de datos se cierre al salir.
        """
        self.db.close()
        event.accept()