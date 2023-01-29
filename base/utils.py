import spacy
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd 
from neuralprophet import NeuralProphet

CATEGORIES = ['food', 'travel', 'bills', 'clothes', 'groceries', 'extra']

def makeJson(text):
    output = {}
    # Load the spaCy model
    nlp = spacy.load("en_core_web_sm")
    
    category = None
    
    for word in text.split():
        if word in CATEGORIES:
            category = word
            break

    # Process the text
    doc = nlp(text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # POS tag the tokens
    tagged_tokens = nltk.pos_tag(tokens)

    # Extract the price
    price = ""
    for token in doc:
        if token.like_num:
            price = token.text
            break

    # Extract the name
    name = ""
    for token, tag in tagged_tokens:
        if tag == "NNS":
            name = token
            break
        if tag == "NN":
            name = token
            break

    output["name"] = name
    output["price"] = price
    
    if category is not None:
        output["category"] = category

    return output


def future_expense(df,period=7):
    #  create a model using neural prophet to predict the amount of money spent on groceries in the future

    data = df[["Date", "Amount"]]     
    data.rename(columns={"Date": "ds", "Amount": "y"}, inplace=True)    
    print(data)
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
