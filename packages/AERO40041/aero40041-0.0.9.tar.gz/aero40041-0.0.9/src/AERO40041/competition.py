import pandas as pd
from sklearn.metrics import accuracy_score

def testTitanicModel(model, preprocess):
    df = pd.read_csv('https://raw.githubusercontent.com/AlexSkillen/AlexSkillen.github.io/refs/heads/main/AERO40041/TitanicTest.csv')

    df = preprocess(df)
    
    df = df.dropna( axis=0)
    
    y = df['Survived'].copy() 
    X = df.loc[:, df.columns != 'Survived'].copy()  

    y_hat = model.predict(X)

    # Compute accuracy
    accuracy = accuracy_score(y, y_hat)

    return accuracy
