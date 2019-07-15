import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('datapokemon.csv')

dfX = df.drop(['Unnamed: 0','idpoke1','idpoke2','winner'], axis='columns')
# print(dfX.columns.values)

dfY = df['winner']

from sklearn.model_selection import train_test_split
xtr, xts, ytr,yts = train_test_split(
    dfX,
    dfY,
    test_size = 0.25
)

model=RandomForestClassifier(n_estimators=20)
model.fit(xtr, ytr)
print(model.score(xts, yts))

import joblib
joblib.dump(model,'modeljoblib')