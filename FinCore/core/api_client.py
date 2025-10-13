import yfinance as yf


def fetch_stock_data(ticker):
    ticker_data = yf.Ticker(ticker)
    """Fetch stock data from Yahoo Finance."""
    # 1. Obtener datos históricos del mercado (precios de cierre, apertura, volumen, etc.)
    # Puedes especificar el periodo (period) y el intervalo (interval)
    # period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    historial = ticker_data.history(period="1mo")
    print("--- Datos Históricos (último mes) ---")
    print(historial.head()) # .head() muestra las primeras 5 filas

    # 2. Obtener información general de la empresa
    info = ticker_data.info
    print(f"\n--- Información General de {info['shortName']} ---")
    print(f"Sector: {info['sector']}")
    print(f"Sitio Web: {info['website']}")
    print(f"Resumen: {info['longBusinessSummary'][:200]}...") # Muestra los primeros 200 caracteres

    # 3. Obtener los dividendos y splits de acciones
    dividendos = ticker_data.dividends
    print("\n--- Próximos Dividendos ---")
    print(dividendos.tail()) # .tail() muestra las últimas 5 filas

fetch_stock_data("AAPL")  