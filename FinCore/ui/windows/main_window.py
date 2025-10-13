import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QDialog, 
    QVBoxLayout, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import QDate

# Importa el gestor de la base de datos
from ...core.database import DatabaseManager 
from ..generated.Ui_main_window import Ui_MainWindow

# --- Ventana Emergente para Añadir Acciones ---
class AddStockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Nueva Acción")

        # Layout principal del diálogo
        self.layout = QVBoxLayout(self)
        
        # Formulario para los datos de la acción
        self.formLayout = QFormLayout()
        self.ticker_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()
        
        self.formLayout.addRow("Ticker:", self.ticker_input)
        self.formLayout.addRow("Cantidad:", self.quantity_input)
        self.formLayout.addRow("Precio de Compra:", self.price_input)
        
        self.layout.addLayout(self.formLayout)
        
        # Botones de Aceptar y Cancelar
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        self.layout.addWidget(self.buttons)

    def get_data(self):
        """Devuelve los datos introducidos en el formulario."""
        return {
            "ticker": self.ticker_input.text().upper(),
            "quantity": self.quantity_input.text(),
            "price": self.price_input.text(),
            "date": QDate.currentDate().toString("yyyy-MM-dd") # Fecha actual
        }

# --- Ventana Principal de la Aplicación ---
class FinancialTerminalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = DatabaseManager()
        self._init_ui()
        self._connect_signals()
        self.display_portfolio_view() # Muestra la vista inicial del portafolio

    def _init_ui(self):
        self.setWindowTitle("FinCore Terminal")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        style_sheet_path = os.path.join(script_dir, "..", "..", "assets", "styles", "styles.qss")
        self.load_style_sheet(style_sheet_path)
    
    def _connect_signals(self):
        """Conecta las señales de los widgets a las funciones."""
        self.ui.miPortafolioButton.clicked.connect(self.display_portfolio_view)

    def display_portfolio_view(self):
        """Limpia y muestra la vista del portafolio en StockLayout."""
        # 1. Limpiar el layout por completo
        while self.ui.StockLayout.count():
            item = self.ui.StockLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # 2. Crear y añadir el botón "Agregar Acción"
        self.add_stock_button = QPushButton("➕ Agregar Acción")
        self.add_stock_button.clicked.connect(self.open_add_stock_dialog)
        self.ui.StockLayout.addWidget(self.add_stock_button)
        
        # 3. Cargar y mostrar las acciones existentes
        stocks = self.db.get_all_stocks()
        
        if not stocks:
            self.ui.StockLayout.addWidget(QLabel("No hay acciones registradas."))
        else:
            for stock in stocks:
                ticker, quantity, price, _ = stock
                stock_label = QLabel(f"{ticker}\nCant: {quantity} | Precio: ${price:.2f}")
                self.ui.StockLayout.addWidget(stock_label)
        
        print("Vista del portafolio actualizada.")

    def open_add_stock_dialog(self):
        """Abre la ventana emergente para añadir una nueva acción."""
        dialog = AddStockDialog(self)
        
        # Si el usuario hace clic en "Ok"
        if dialog.exec():
            data = dialog.get_data()
            try:
                # Validar y convertir datos
                ticker = data['ticker']
                quantity = int(data['quantity'])
                price = float(data['price'])
                
                if not ticker: # Simple validación
                    raise ValueError("El ticker no puede estar vacío.")

                # Añadir a la base de datos
                self.db.add_stock(ticker, quantity, price, data['date'])
                QMessageBox.information(self, "Éxito", f"Acción {ticker} añadida correctamente.")
                
                # Refrescar la vista del portafolio
                self.display_portfolio_view()

            except ValueError as e:
                QMessageBox.warning(self, "Error de Entrada", f"Datos inválidos: {e}")
            except Exception as e:
                QMessageBox.critical(self, "Error en la Base de Datos", f"No se pudo añadir la acción: {e}")

    def load_style_sheet(self, path):
        try:
            with open(path, "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Ocurrió un error al cargar los estilos: {e}")
            
    def closeEvent(self, event):
        self.db.close()
        event.accept()