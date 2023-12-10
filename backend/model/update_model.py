from moexalgo import Market, Ticker
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import keras
from keras import layers
from keras.models import Model
import matplotlib.pyplot as plt

# Function that splits the dataset into 2 based on the given time step.
def create_dataset_with_timesteps(data, time_step=60):
    data_X, data_y = [], []
    for i in range(len(data) - time_step - 1):
        point = data[i:(i + time_step), 0]
        data_X.append(point)
        data_y.append(data[i + time_step, 0])
    return np.array(data_X), np.array(data_y)

# Function that creates an LSTM.
def define_LSTM_model_v1(number_of_lstm_units, input_shape):
    # Define input layer.
    input_layer = layers.Input(shape=input_shape)
    
    # Define the LSTM layers.
    lstm1 = layers.LSTM(number_of_lstm_units, return_sequences=True)(input_layer)
    lstm2 = layers.LSTM(number_of_lstm_units, return_sequences=True)(lstm1)
    lstm3 = layers.LSTM(number_of_lstm_units)(lstm2)
    
    # Define the output layer.
    output_layer = layers.Dense(1)(lstm3)
    
    # Create the model.
    return Model(inputs=input_layer, outputs=output_layer)

# Sber ticker.
sber = Ticker('MOEX')

# Import all stocks.
stocks = Market('stocks')

# Sber candles.
s_stock_data = pd.DataFrame(sber.candles(date='2021-11-17', till_date='today', period='1h'))

#print(s_stock_data.tail())

# Check if there is any missing data.
if len(s_stock_data.isna().sum().unique()) > 1:
    print("Missing data found.")
    exit(0)

# Define a "target" series that contains "close" column from the dataset.
# Time - closing time of the candle.
target = s_stock_data['close']
close_time = s_stock_data['end']

# Scale the variables.
min_max_scaler = MinMaxScaler()
target_scaled = min_max_scaler.fit_transform(np.array(target).reshape(-1, 1))

# Split data into training and test sets.
split_ratio = 0.85
X, y = create_dataset_with_timesteps(target_scaled, 100)

# Define the model.
close_model_v1 = define_LSTM_model_v1(50, input_shape=(X.shape[1], 1))

# Compile the model.
close_model_v1.compile(loss='mean_squared_error', optimizer='adam')

# The summary of the model
#close_model_v1.summary()

# Train the model.
close_model_v1.fit(X, y, batch_size=64, epochs=100, verbose=1)

# Save the model.
close_model_v1.save('/Users/timurzeksimbaev/Desktop/Go-ALGO/backend/home/close_model_MOEX.keras')
