import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="fincore.db"):
        """
        Inicializa el gestor de la base de datos.
        Crea la base de datos y las tablas si no existen.
        """
        # Crear un directorio 'data' en la raíz del proyecto si no existe
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        data_dir = os.path.join(project_root, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        self.db_path = os.path.join(data_dir, db_name)
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.create_tables()
            print(f"Base de datos conectada exitosamente en: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")

    def create_tables(self):
        """
        Crea las tablas necesarias si no existen.
        """
        if not self.conn:
            return
            
        cursor = self.conn.cursor()
        # Ejemplo: Tabla para guardar acciones (portfolio)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL,
                purchase_price REAL NOT NULL,
                purchase_date TEXT
            )
        ''')
        self.conn.commit()
        print("Tabla 'portfolio' creada o ya existente.")

    def add_stock(self, ticker, quantity, purchase_price, purchase_date):
        """
        Añade una nueva acción a la tabla portfolio.
        """
        if not self.conn:
            return None
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO portfolio (ticker, quantity, purchase_price, purchase_date)
                VALUES (?, ?, ?, ?)
            ''', (ticker, quantity, purchase_price, purchase_date))
            self.conn.commit()
            print(f"Acción {ticker} añadida al portfolio.")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al añadir la acción: {e}")
            return None

    def get_all_stocks(self):
        """
        Obtiene todas las acciones del portfolio.
        """
        if not self.conn:
            return []
            
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ticker, quantity, purchase_price, purchase_date FROM portfolio")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener las acciones: {e}")
            return []

    def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.conn:
            self.conn.close()
            print("Conexión con la base de datos cerrada.")