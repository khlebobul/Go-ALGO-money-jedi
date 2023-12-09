import os
#tf_enable_onednn = os.environ.get("TF_ENABLE_ONEDNN_OPTS")
#tf_enable_onednn = 0

from moexalgo import Market, Ticker
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
#import tensorflow as tf
from tensorflow.keras import layers
import keras
from tensorflow.keras.models import Model
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

from datetime import datetime, timedelta
import pandas as pd

# Function to generate timeslots
def generate_timeslots(input_time, num_slots):

    # Parse the input time to a datetime object
    start_time = datetime.strptime(input_time, '%Y-%m-%d %H:%M:%S')
    
    # Initialize the list of timeslots with the input_time
    timeslots = [start_time]
    
    # Generate timeslots
    for _ in range(1, num_slots):
        # Add 1 hour to the last timeslot
        next_slot = timeslots[-1] + timedelta(hours=1)
        
        # If the next timeslot goes past 18:59:59, reset to the next day at 09:59:59
        if next_slot.time() > datetime.strptime("18:59:59", "%H:%M:%S").time():
            next_slot = datetime.combine(next_slot.date() + timedelta(days=1),
                                         datetime.strptime("09:59:59", "%H:%M:%S").time())
        
        # Append the new timeslot to the list
        timeslots.append(next_slot)
    
    # Return the timeslots as a pandas Series
    return pd.Series(timeslots, name='end')

# Sber ticker.
sber = Ticker('SBER')

# Import all stocks.
stocks = Market('stocks')

# Sber candles.
s_stock_data = pd.DataFrame(sber.candles(date='2021-11-17', till_date='2023-09-11', period='1h'))

#print(s_stock_data.tail())

# Check if there is any missing data.
if len(s_stock_data.isna().sum().unique()) > 1:
    print("Missing data found.")
    exit(0)

# Define a "target" series that contains "close" column from the dataset.
# Time - closing time of the candle.
target = s_stock_data['close']
close_time = s_stock_data['end']

# Variable that decides how many hours do we want account.
number_of_hours = 100

# Scale the variables.
min_max_scaler = MinMaxScaler()
target_scaled = min_max_scaler.fit_transform(np.array(target).reshape(-1, 1))

# Split data into training and test sets.
X, y = create_dataset_with_timesteps(target_scaled, number_of_hours)

# Save the model.
close_model_v1 = keras.models.load_model('close_model_v1.keras')


# Define the number of hours for prediction.
number_of_hours_predicted = 5

# "number_of_hours_predicted" cannot exceed "number_of_hours".
if number_of_hours_predicted > number_of_hours:
    print("Number of predicted days cannot exceed number of days used for prediction.")

# Generate predictions for the next "number_of_hours_predicted" hours.
X_old = X[-1]
for i in range(number_of_hours_predicted):
    
    # Define X_new.
    X_new = X_old
    
    # Generate y_new.
    y_new = close_model_v1.predict(X_new.reshape(-1, 100, 1))
    
    X_old = np.append(X_old[-99:], y_new)

# Scale back the result.
target_final = pd.Series(min_max_scaler.inverse_transform(X_old[-1 * number_of_hours_predicted:].reshape(-1, 1)).reshape(-1, ), name='close')

# Form a Dataframe that contains predicted price.
time_slot = str(close_time[-1:].values[0]).split('T')[0] + ' ' + str(close_time[-1:].values[0]).split('T')[1].split('.')[0]

predicted_timeslots = generate_timeslots(time_slot, number_of_hours_predicted + 1)[1:].reset_index()

predicted_df = pd.concat([predicted_timeslots, target_final.apply(lambda x: round(x, 2))], axis=1).drop(columns=['index'], axis=1)



#
# This is our predictions.
#
print(predicted_df)



# Create an original df.
original_df = pd.concat([close_time, target], axis=1)[-5:].reset_index().drop(columns=['index'], axis=1)



#
# This is the real prices.
#
print(original_df)