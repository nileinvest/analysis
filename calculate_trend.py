import yfinance as yf
import pandas_ta as ta
import pandas as pd
import json

# 1. Legge in automatico il file caricato su GitHub
# (Assicurati che il nome qui sotto corrisponda a quello del file caricato)
df_assets = pd.read_csv('assets.csv')

# 2. Estrae la colonna "Ticker" ignorando eventuali spazi vuoti
tickers = df_assets.dropna().astype(str).str.strip().tolist()

results =

for ticker in tickers:
    print(f"Elaborazione di {ticker}...")
    try:
        # Scarica i dati storici degli ultimi 6 mesi
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        if df.empty:
            print(f"Nessun dato trovato per {ticker}.")
            continue

        # Calcola il SuperTrend (Parametri: ATR 11, Moltiplicatore 3, sorgente H+L/2 implicita)
        supertrend_data = ta.supertrend(df['High'], df['Low'], df['Close'], length=11, multiplier=3)
        
        # Unisce i dati e rimuove le righe vuote iniziali
        df = pd.concat([df, supertrend_data], axis=1).dropna()
        
        if df.empty:
            continue
            
        # Prende l'ultima candela disponibile (il dato più recente)
        last_row = df.iloc[-1]
        
        # La direzione del SuperTrend (1 = Bullish, -1 = Bearish)
        trend_direction = last_row
        
        if trend_direction == 1:
            trend_status = "BULLISH"
        else:
            trend_status = "BEARISH"
            
        # Prepara i dati per il grafico interattivo (estrae le ultime 60 candele)
        chart_data =
        for index, row in df.tail(60).iterrows():
            chart_data.append({
                "time": index.strftime('%Y-%m-%d'),
                "open": float(row['Open'].iloc) if isinstance(row['Open'], pd.DataFrame) else float(row['Open']),
                "high": float(row['High'].iloc) if isinstance(row['High'], pd.DataFrame) else float(row['High']),
                "low": float(row['Low'].iloc) if isinstance(row['Low'], pd.DataFrame) else float(row['Low']),
                "close": float(row['Close'].iloc) if isinstance(row['Close'], pd.DataFrame) else float(row['Close']),
                "supertrend": float(row)
            })
            
        results.append({
            "ticker": ticker,
            "trend": trend_status,
            "last_price": float(last_row['Close'].iloc) if isinstance(last_row['Close'], pd.DataFrame) else float(last_row['Close']),
            "chart_data": chart_data
        })
        
    except Exception as e:
        print(f"Errore durante l'elaborazione di {ticker}: {e}")

# Salva i dati finali nel file JSON che alimenterà la dashboard
with open('data.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Calcoli terminati. Dati salvati in data.json con successo!")
