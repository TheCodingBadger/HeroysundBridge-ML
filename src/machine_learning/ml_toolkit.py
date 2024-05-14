import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas as pd
from tensorflow.keras.losses import mean_squared_error, mean_absolute_error
from sklearn.metrics import r2_score as score

def df_to_X_y(dataset, window_size = 6):
    X = []
    y = []
    for i in range(window_size, len(dataset)):
        X.append(dataset.iloc[i-window_size:i, 1:].values)  # Use all columns except 'Point_1_N_mean' as input
        y.append(dataset.iloc[i, 0])  # Use 'Point_1_N_mean' as output
    a = np.array(X)
    b= np.array(y)
    return a, b

# Plot the predictions of the model
def plot_predictions(dataset, split, model, X, y, start=0, end=100, scaler=None):
    predictions = model.predict(X).flatten()
    predictions = predictions.reshape(-1, 1) 
    if scaler is not None:
        predictions = scaler.inverse_transform(predictions)
    df = pd.DataFrame(data={'Predictions': predictions.flatten(),'Actuals': y})
    plt.figure(figsize=(12, 5))
    plt.plot(dataset[-split:].index,df['Actuals'][start:end], label='Test Dataset')
    plt.plot(dataset[-split:].index,df['Predictions'][start:end], label='ML Predictions')
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.xlabel('Date',fontsize=16)
    plt.ylabel("'Point_1_N_mean' Strain [μm/m]",fontsize=16)
    plt.legend(fontsize=14)
    plt.show()
    print(f"MSE: {mean_squared_error(df['Actuals'][start:end], df['Predictions'][start:end])}")
    print(f"MAE: {mean_absolute_error(df['Actuals'][start:end], df['Predictions'][start:end])}")
    print(f"R^2 Score: {score(df['Actuals'][start:end], df['Predictions'][start:end])}")
    display(df)


# Plot on validation set
def plot_predictions_1(dataset, split, model, X, y, start=0, end=100, scaler=None):
    predictions = model.predict(X).flatten()
    predictions = predictions.reshape(-1, 1) 
    if scaler is not None:
        predictions = scaler.inverse_transform(predictions)
    df = pd.DataFrame(data={'Predictions': predictions.flatten(),'Actuals': y})
    plt.figure(figsize=(10, 5))
    plt.plot(dataset[split[0]:-split[2]].index,df['Actuals'][start:end])
    plt.plot(dataset[split[0]:-split[2]].index,df['Predictions'][start:end])
    plt.show()
    print(f"MSE: {mean_squared_error(df['Actuals'][start:end], df['Predictions'][start:end])}")
    print(f"MAE: {mean_absolute_error(df['Actuals'][start:end], df['Predictions'][start:end])}")
    print(f"R^2 Score: {score(df['Actuals'][start:end], df['Predictions'][start:end])}")
    display(df)