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
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    # Calcular indicadores y señales de trading
    df['Volume_SMA'] = df['volume'].rolling(window=20).mean()
    df['Body'] = abs(df['close'] - df['open'])
    df['Small_Body'] = df['Body'] < 0.2 * df['Body'].mean()  # Cuerpo pequeño en comparación con la media de los cuerpos
    df['Regular_Shadows'] = (df['high'] - df['close']).abs() < 0.2 * df['close']  # Sombras regulares
    df['High_Volume'] = df['volume'] > df['Volume_SMA']  # Volumen alto respecto a la media móvil

    # Filtrar para obtener solo las velas con cuerpo pequeño, sombras regulares y alto volumen
    df_filtered = df[df['High_Volume'] & df['Small_Body'] & df['Regular_Shadows']]

    # Graficar velas japonesas con volumen en la parte inferior
    mc = mpf.make_marketcolors(up='g', down='r', volume='in')
    s = mpf.make_mpf_style(marketcolors=mc)

    # Crear el gráfico con mplfinance
    fig, axlist = mpf.plot(df, type='candle', volume=True, style=s, returnfig=True)

    # Agregar marcadores para señalar las velas con alto volumen, cuerpo pequeño y sombras regulares
    ax = axlist[0]
    for i in range(len(df_filtered)):
        # Obtener la posición en el eje x de la vela filtrada
        index_pos = df.index.get_loc(df_filtered.index[i])
        # Añadir un marcador en la posición de la vela filtrada
        ax.annotate('High Vol, Small Body, Regular Shadows',
                    xy=(index_pos, df_filtered['high'].iloc[i]),
                    xytext=(index_pos, df_filtered['high'].iloc[i] + (df['high'].max() - df['low'].min()) * 0.1),
                    color='blue',
                    fontsize=10,
                    ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.4', fc='yellow', alpha=0.5),
                    arrowprops=dict(facecolor='blue', arrowstyle='->', connectionstyle='arc3,rad=0'))

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

import asyncio
import requests
import pandas as pd
from datetime import datetime, timedelta
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import create_engine

# Define la URL de la API de Binance
base_url = 'https://api.binance.com'
endpoint = '/api/v3/klines'

# Configuración de la conexión a la base de datos MySQL
db_user = 'root'
db_password = '21blackjack'
db_host = 'localhost'
db_database = 'sql1'
table_name = 'prediction_example'

# Crea la conexión a la base de datos usando sqlalchemy
engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_database}")

# Función para obtener los datos y hacer la predicción
async def get_prediction_and_save_to_db():
    try:
        # Define los parámetros para la solicitud
        symbol = 'BTCUSDT'
        interval = '5m'
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=6)

        end_time_ms = int(end_time.timestamp() * 1000)
        start_time_ms = int(start_time.timestamp() * 1000)

        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time_ms,
            'endTime': end_time_ms,
            'limit': 72
        }

        response = requests.get(base_url + endpoint, params=params)
        data = response.json()

        columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
                   'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
        df = pd.DataFrame(data, columns=columns)

        df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
        df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')

        df = df[['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df.set_index('Open Time', inplace=True)

        df = df.astype(float)

        df['Direction'] = df['Close'].diff().apply(lambda x: 1 if x > 0 else 0).shift(-1)
        df.dropna(inplace=True)

        explanatory = df.drop(columns='Direction')
        target = df['Direction']

        model = DecisionTreeClassifier(max_depth=4)
        model.fit(X=explanatory, y=target)

        latest_data = explanatory.iloc[-1].to_frame().T
        prediction = model.predict(latest_data)[0]
        score = model.score(X=explanatory, y=target)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        close_price = latest_data['Close'].values[0]
        prediction_result = "El precio subirá." if prediction == 1 else "El precio bajará."

        # Imprimir la información incluyendo el score del modelo
        print(f"{current_time} - Close Price: {close_price}, Prediction: {prediction_result}, Model Score: {score}")
        
        # Guardar en la base de datos
        df_to_save = pd.DataFrame({
            'timestamp': [current_time],
            'close_price': [close_price],
            'prediction': [prediction_result],
            'model_score': [score]
        })

        df_to_save.to_sql(name=table_name, con=engine, if_exists='append', index=True, index_label='Date')

    except Exception as e:
        print(f"Error: {e}")

# Función que ejecuta get_prediction_and_save_to_db() cada 5 minutos
async def main():
    while True:
        await get_prediction_and_save_to_db()
        await asyncio.sleep(300)  # Espera 5 minutos antes de la siguiente ejecución

# Ejecutar el bucle principal usando asyncio en Jupyter Lab
await main()