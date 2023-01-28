
import pandas as pd 
from neuralprophet import NeuralProphet

def future_expense(df,period=7):
    #  create a model using neural prophet to predict the amount of money spent on groceries in the future
    
    data = df[["Date", "Amount"]]         
    data.rename(columns={"Date": "ds", "Amount": "y"}, inplace=True)
    # model creation
    model = NeuralProphet(

        growth="linear",  # Determine trend types: 'linear', 'discontinuous', 'off'
        changepoints=None, # list of dates that may include change points (None -> automatic )
        n_changepoints=5,
        changepoints_range=0.8,
        trend_reg=0,
        trend_reg_threshold=False,
        yearly_seasonality="auto",
        weekly_seasonality="auto",
        daily_seasonality="auto",
        seasonality_mode="additive",
        seasonality_reg=0,
        n_forecasts=1,
        n_lags=0,
        num_hidden_layers=0,
        d_hidden=None,     # Dimension of hidden layers of AR-Net
    
        learning_rate=None,
        epochs=40,
        loss_func="Huber",
        normalize="auto",  # Type of normalization ('minmax', 'standardize', 'soft', 'off')
        impute_missing=True,)

    metrics = model.fit(data,  freq="D") 
    future = model.make_future_dataframe(data, periods=period, n_historic_predictions=False) 
    forecast = model.predict(future)
    return forecast["yhat1"]