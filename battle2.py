from flask import redirect, request, Flask, render_template, url_for, send_from_directory, abort
import json, requests
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os, random

app = Flask(__name__)
app.config['upload_folder']='storage'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hasil', methods=['POST','GET'])
def post():
    model = joblib.load('modeljoblib')

    poke1 = request.form['pokemon1']
    poke2 = request.form['pokemon2']
    poke1 = poke1.lower()
    poke2 = poke2.lower()

    if poke1 == "":
        return render_template('notfound.html')
    else:
        if poke2 == "":
            return render_template('notfound.html')
        else:
            datapokemon = pd.read_csv('pokemon.csv')
            
            idpoke1 = (datapokemon[datapokemon['Name'] == poke1.title()].index.values[0]) + 1
            idpoke2 = (datapokemon[datapokemon['Name'] == poke2.title()].index.values[0]) + 1

            url1 = 'https://pokeapi.co/api/v2/pokemon/'+ poke1
            url2 = 'https://pokeapi.co/api/v2/pokemon/'+ poke2
            data1 = requests.get(url1)
            data2 = requests.get(url2)

            if str(data1)=='<Response [404]>':
                abort(404)
            else:
                gambar1 = data1.json()['sprites']['front_default']
        
            if str(data2)=='<Response [404]>':
                abort(404)
            else:
                gambar2 = data2.json()['sprites']['front_default']

            dfpoke = pd.read_csv('pokemon.csv',index_col=0)

            hp1 = dfpoke.loc[idpoke1]['HP']
            hp2 = dfpoke.loc[idpoke2]['HP']
            att1 = dfpoke.loc[idpoke1]['Attack']
            att2 = dfpoke.loc[idpoke2]['Attack']
            def1 = dfpoke.loc[idpoke1]['Defense']
            def2 = dfpoke.loc[idpoke2]['Defense']
            spatt1 = dfpoke.loc[idpoke1]['Sp. Atk']
            spatt2 = dfpoke.loc[idpoke2]['Sp. Atk']
            spdef1 = dfpoke.loc[idpoke1]['Sp. Def']
            spdef2 = dfpoke.loc[idpoke2]['Sp. Def']
            speed1 = dfpoke.loc[idpoke1]['Speed']
            speed2 = dfpoke.loc[idpoke2]['Speed']

            predict = model.predict([[hp1, hp2, att1, att2, def1, def2, spatt1, spatt2, spdef1, spdef2, speed1, speed2]])[0]
            if predict == 0:
                winner = poke1.title()
            else:
                winner = poke2.title()

            proba = model.predict_proba([[hp1, hp2, att1, att2, def1, def2, spatt1, spatt2, spdef1, spdef2, speed1, speed2]])
            probamax = round(proba[0, predict] * 100, 0)

            plt.close()
            plt.figure('Battle Result', figsize=(20,10))
            plt.subplot(1, 6, 1)
            plt.title('HP')
            plt.bar(
                poke1,
                hp1,
                width= 1
            )
            plt.bar(
                poke2,
                hp2,
                width= 1
            )

            plt.subplot(1, 6, 2)
            plt.title('Attack')
            plt.bar(
                poke1,
                att1,
                width= 1
            )
            plt.bar(
                poke2,
                att2,
                width= 1
            )

            plt.subplot(1, 6, 3)
            plt.title('Defense')
            plt.bar(
                poke1,
                def1,
                width= 1
            )
            plt.bar(
                poke2,
                def2,
                width= 1
            )

            plt.subplot(1, 6, 4)
            plt.title('Special Attack')
            plt.bar(
                poke1,
                spatt1,
                width= 1
            )
            plt.bar(
                poke2,
                spatt2,
                width= 1
            )

            plt.subplot(1, 6, 5)
            plt.title('Special Defense')
            plt.bar(
                poke1,
                spdef1,
                width= 1
            )
            plt.bar(
                poke2,
                spdef2,
                width= 1
            )

            plt.subplot(1, 6, 6)
            plt.title('Speed')
            plt.bar(
                poke1,
                speed1,
                width= 1
            )
            plt.bar(
                poke2,
                speed2,
                width= 1
            )

            address = './storage/' + poke1 + 'vs' + poke2 +'.png'
            urlgraph ='http://localhost:5000/graph/'+ poke1 +'vs'+ poke2 +'.png'
            plt.savefig(address)
            graph = urlgraph

            plt.close()
            return render_template('pokemon.html',nama1=poke1.title(),nama2=poke2.title(),gambar1=gambar1,gambar2=gambar2,winner=winner,proba=probamax, graph = graph)

@app.route('/graph/<path:x>')
def graph(x):
    return send_from_directory('storage', x)

@app.errorhandler(404)
def notFound404(x):
    return render_template('notfound.html')

if __name__=='__main__':
    app.run(debug=True)