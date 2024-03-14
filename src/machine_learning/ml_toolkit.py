def df_to_X_y(dataset, window_size = 6):
    X = []
    y = []
    for i in range(window_size, len(dataset)):
        X.append(dataset.iloc[i-window_size:i, 1:].values)  # Use all columns except 'Point_1_N_mean' as input
        y.append(dataset.iloc[i, 0])  # Use 'Point_1_N_mean' as output
    return np.array(X), np.array(y)

def plot_predictions(model, X, y, start=0, end=100):
    predictions = model.predict(X).flatten()
    predictions = predictions.reshape(-1, 1)  # Corrected line
    predictions = scaler_y.inverse_transform(predictions)
    df = pd.DataFrame(data={'Predictions': predictions.flatten(),'Actuals': y})
    plt.plot(df['Actuals'][start:end])
    plt.plot(df['Predictions'][start:end])
    return df, mse(y, predictions)