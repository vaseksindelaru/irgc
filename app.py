from flask import Flask, send_file, send_from_directory
from flask_cors import CORS
import ccxt
import pandas as pd
import mplfinance as mpf
import io
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

@app.route('/')
def index():
    return '''
    <h1>Welcome to the Flask Server</h1>
    <p>Go to <a href="/plot.png">/plot.png</a> to see the plot.</p>
    '''

@app.route('/plot.png')
def plot():
    # Obtener datos de Binance usando ccxt
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'
    timeframe = '5m'
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=200)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    # Calcular indicadores y señales de trading
    df['Volume_SMA'] = df['volume'].rolling(window=20).mean()
    df['Body'] = abs(df['close'] - df['open'])
    df['Upper_Shadow'] = df['high'] - df[['close', 'open']].max(axis=1)
    df['Lower_Shadow'] = df[['close', 'open']].min(axis=1) - df['low']
    df['Range'] = df['high'] - df['low']
    df['High_Volume'] = df['volume'] > df['Volume_SMA']
    df['Small_Candle'] = df['Body'] < 0.2 * df['Range']
    df['Trade_Signal'] = df['High_Volume'] & df['Small_Candle']

    # Análisis de dirección
    def analyze_direction(df, period=10):
        results = {'Signal Time': [], 'Direction Before': [], 'Direction After': []}
        for i in range(period, len(df)):
            if df['Trade_Signal'].iloc[i]:
                previous_closes = df['close'].iloc[i-period:i]
                after_closes = df['close'].iloc[i:i+period]
                direction_before = 'Up' if previous_closes.iloc[-1] > previous_closes.iloc[0] else 'Down'
                direction_after = 'Up' if after_closes.iloc[-1] > after_closes.iloc[0] else 'Down'
                results['Signal Time'].append(df.index[i])
                results['Direction Before'].append(direction_before)
                results['Direction After'].append(direction_after)
        return pd.DataFrame(results)

    analysis_df = analyze_direction(df)
    prob_up = (analysis_df['Direction Before'] == analysis_df['Direction After']).mean()
    prob_down = 1 - prob_up

    # Graficar velas japonesas con volumen en la parte inferior
    mc = mpf.make_marketcolors(up='g', down='r', volume='in')
    s = mpf.make_mpf_style(marketcolors=mc)
    
    # Crear el gráfico con mplfinance
    fig, axlist = mpf.plot(df, type='candle', volume=True, style=s, returnfig=True)
    
    # Guardar el gráfico en un archivo temporal
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        fig.savefig(tmp_file, format='png')

    # Enviar el archivo temporal como respuesta
    return send_file(tmp_file.name, mimetype='image/png')

# Manejar la solicitud de favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
