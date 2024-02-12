import pandas as pd
from time import *
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.config["DEBUG"] = False


@app.route('/')
def form():
    return render_template('Formulaire.html')


@app.route('/', methods=['POST'])
def traitementDonnes():
    date = request.form['date']
    url = f"https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/{date[6:]}/FR_E2_{date[6:]}-{date[3:5]}-{date[:2]}.csv"
    donnees = pd.read_csv(url, sep=';')
    donneesSite = donnees[donnees['nom site'] == "VITRY-SUR-SEINE"]
    dates = list(set(donneesSite["Date de début"]))
    dates.sort()
    polluant = list(set(donneesSite["Polluant"]))
    polluant.sort()
    dico = {p: list(donneesSite[donneesSite.Polluant == p].valeur)
            for p in polluant}
    dataFrame = pd.DataFrame(dico, index=dates)
    graph = dataFrame.plot()
    plt.savefig('./static/graph.png')
    return render_template('result.html', data=dataFrame.to_html(), img='./static/graph.png')


if __name__ == '__main__':
    app.run()
