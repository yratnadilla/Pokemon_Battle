import pandas as pd

dfPokemon = pd.read_csv('pokemon.csv',index_col=0)
dfPokemon = dfPokemon[['Name','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']]
dfCombats = pd.read_csv('combats.csv')

id1 = []
id2 = []
hp1 = []
hp2 = []
att1 = []
att2 = []
def1 = []
def2 = []
spatt1 = []
spatt2 = []
spdef1 = []
spdef2 = []
speed1 = []
speed2 = []
winner = []

for i in range(len(dfCombats)):
    idpoke1 = dfCombats.iloc[i]['First_pokemon']
    idpoke2 = dfCombats.iloc[i]['Second_pokemon']
    winners = dfCombats.iloc[i]['Winner']

    id1.append(idpoke1)
    id2.append(idpoke2)
    hp1.append(dfPokemon.loc[idpoke1]['HP'])
    hp2.append(dfPokemon.loc[idpoke2]['HP'])
    att1.append(dfPokemon.loc[idpoke1]['Attack'])
    att2.append(dfPokemon.loc[idpoke2]['Attack'])
    def1.append(dfPokemon.loc[idpoke1]['Defense'])
    def2.append(dfPokemon.loc[idpoke2]['Defense'])
    spatt1.append(dfPokemon.loc[idpoke1]['Sp. Atk'])
    spatt2.append(dfPokemon.loc[idpoke2]['Sp. Atk'])
    spdef1.append(dfPokemon.loc[idpoke1]['Sp. Def'])
    spdef2.append(dfPokemon.loc[idpoke2]['Sp. Def'])
    speed1.append(dfPokemon.loc[idpoke1]['Speed'])
    speed2.append(dfPokemon.loc[idpoke2]['Speed'])

    if winners == idpoke1:
        win = 0
        winner.append(win)
    else:
        win = 1
        winner.append(win)

df = pd.DataFrame(
    dict(
        idpoke1 = id1,
        idpoke2 = id2,
        hp1 = hp1,
        hp2 = hp2,
        att1 = att1,
        att2 = att2,
        def1 = def1,
        def2 = def2,
        spatt1 = spatt1,
        spatt2 = spatt2,
        spdef1 = spdef1,
        spdef2 = spdef2,
        speed1 = speed1,
        speed2 = speed2,
        winner = winner
    )
)

df.to_csv('datapokemon.csv')