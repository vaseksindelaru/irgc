from flask import Flask, send_file
from flask_cors import CORS
import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

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
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=1000)
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

    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['close'], label='Close Price', color='blue')
    plt.scatter(analysis_df[analysis_df['Direction After'] == 'Up']['Signal Time'], 
                df.loc[analysis_df[analysis_df['Direction After'] == 'Up']['Signal Time'], 'close'], 
                color='green', label='Signal - Up', marker='^', alpha=1)
    plt.scatter(analysis_df[analysis_df['Direction After'] == 'Down']['Signal Time'], 
                df.loc[analysis_df[analysis_df['Direction After'] == 'Down']['Signal Time'], 'close'], 
                color='red', label='Signal - Down', marker='v', alpha=1)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Trading Signals and Price Direction Analysis')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gcf().autofmt_xdate()

    # Guardar el gráfico en un objeto BytesIO y enviarlo como respuesta
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
