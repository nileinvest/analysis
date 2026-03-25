import yfinance as yf
import pandas_ta as ta
import pandas as pd
import json

# Lista di aziende di esempio (qui inserirai i ticker delle aziende che ti interessano)
tickers =

results =

for ticker in tickers:
    print(f"Elaborazione di {ticker}...")
    try:
        # Scarica i dati storici degli ultimi 6 mesi (candele giornaliere)
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        if df.empty:
            continue

        # Calcola il SuperTrend con i tuoi parametri esatti: ATR 11, Moltiplicatore 3
        # pandas_ta calcola in automatico la direzione e il valore della linea
        supertrend_data = ta.supertrend(df['High'], df['Low'], df['Close'], length=11, multiplier=3)
        
        # Unisci i dati del SuperTrend al dataframe originale dei prezzi
        df = pd.concat([df, supertrend_data], axis=1)
        
        # Rimuovi i valori nulli iniziali dovuti al calcolo dell'ATR
        df = df.dropna()
        
        # Prendi l'ultima riga (i dati di oggi/dell'ultima chiusura)
        last_row = df.iloc[-1]
        
        # pandas_ta crea una colonna chiamata 'SUPERTd_11_3.0' per la direzione (1 = Bullish, -1 = Bearish)
        trend_direction = last_row
        
        if trend_direction == 1:
            trend_status = "BULLISH"
        else:
            trend_status = "BEARISH"
            
        # Prepariamo i dati per il grafico del sito web (ultime 60 candele per leggerezza)
        chart_data =
        for index, row in df.tail(60).iterrows():
            chart_data.append({
                "time": index.strftime('%Y-%m-%d'),
                "open": float(row['Open'].iloc) if isinstance(row['Open'], pd.Series) else float(row['Open']),
                "high": float(row['High'].iloc) if isinstance(row['High'], pd.Series) else float(row['High']),
                "low": float(row['Low'].iloc) if isinstance(row['Low'], pd.Series) else float(row['Low']),
                "close": float(row['Close'].iloc) if isinstance(row['Close'], pd.Series) else float(row['Close']),
                "supertrend": float(row) # Il valore esatto della linea da disegnare
            })
            
        # Aggiungiamo i risultati di questa azienda alla lista finale
        results.append({
            "ticker": ticker,
            "trend": trend_status,
            "last_price": float(last_row['Close'].iloc) if isinstance(last_row['Close'], pd.Series) else float(last_row['Close']),
            "chart_data": chart_data
        })
        
    except Exception as e:
        print(f"Errore durante l'elaborazione di {ticker}: {e}")

# Salva tutto in un file data.json che verrà letto dal tuo sito web
with open('data.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Calcoli terminati. Dati salvati in data.json con successo!")
