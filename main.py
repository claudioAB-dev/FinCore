import sys
from PyQt6.QtWidgets import QApplication
from FinCore.ui.windows.main_window import FinancialTerminalApp

def main():
    """
    Punto de entrada principal para la aplicación FinCore Terminal.
    """
    app = QApplication(sys.argv)
    window = FinancialTerminalApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()