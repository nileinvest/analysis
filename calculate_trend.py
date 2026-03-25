import yfinance as yf
import pandas_ta as ta
import pandas as pd
import json

# Legge il file e isola esplicitamente la colonna "Ticker"
df_assets = pd.read_csv('asset.csv')
tickers = df_assets.dropna().astype(str).str.strip().tolist()

results =

for ticker in tickers:
    print(f"Elaborazione di {ticker}...")
    try:
        # Scarica i dati storici
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        if df.empty:
            print(f"Nessun dato trovato per {ticker}.")
            continue

        # Calcola il SuperTrend con i tuoi parametri
        supertrend_data = ta.supertrend(df['High'], df['Low'], df['Close'], length=11, multiplier=3)
        df = pd.concat([df, supertrend_data], axis=1).dropna()
        
        if df.empty:
            continue
            
        last_row = df.iloc[-1]
        
        # Estrae la direzione esatta
        trend_direction = last_row
        if isinstance(trend_direction, pd.Series):
            trend_direction = trend_direction.iloc
        
        if trend_direction == 1:
            trend_status = "BULLISH"
        else:
            trend_status = "BEARISH"
            
        # Prepara i dati grafici (ultime 60 candele)
        chart_data =
        for index, row in df.tail(60).iterrows():
            open_val = float(row['Open'].iloc) if isinstance(row['Open'], pd.Series) else float(row['Open'])
            high_val = float(row['High'].iloc) if isinstance(row['High'], pd.Series) else float(row['High'])
            low_val = float(row['Low'].iloc) if isinstance(row['Low'], pd.Series) else float(row['Low'])
            close_val = float(row['Close'].iloc) if isinstance(row['Close'], pd.Series) else float(row['Close'])
            st_val = float(row.iloc) if isinstance(row, pd.Series) else float(row)

            chart_data.append({
                "time": index.strftime('%Y-%m-%d'),
                "open": open_val,
                "high": high_val,
                "low": low_val,
                "close": close_val,
                "supertrend": st_val
            })
            
        last_price = float(last_row['Close'].iloc) if isinstance(last_row['Close'], pd.Series) else float(last_row['Close'])
            
        results.append({
            "ticker": ticker,
            "trend": trend_status,
            "last_price": last_price,
            "chart_data": chart_data
        })
        
    except Exception as e:
        print(f"Errore durante l'elaborazione di {ticker}: {e}")

# Salva i dati
with open('data.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Calcoli terminati. Dati salvati in data.json con successo!")
