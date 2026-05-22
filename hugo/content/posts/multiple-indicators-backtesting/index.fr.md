---
post_kind: article
title: "Backtest d’indicateurs techniques sur plusieurs tickers avec Python"
date: 2024-05-30T15:00:00-04:00
lastmod: 2026-05-23T00:30:00-04:00
description: Expérimentation avec le projet BatchBacktesting — EMA, MACD, APIs FMP/Binance et résultats agrégés sur actions et crypto.
translationKey: multiple-indicators-backtesting
tags:
    - Python
    - Trading
    - Backtesting
    - Crypto
canonicalURL: "https://medium.com/@antoine.boucher012/multiple-technical-indicators-backtesting-on-multiple-tickers-using-python-a5c933d3f1bf"
---

Même stack **[BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting)** que l’[expérience indicateurs]({{< ref "/posts/experimentation-indicateurs-backtesting/index.fr.md" >}}), mais à l’échelle de **nombreux tickers** et actions + crypto — classements agrégés plutôt qu’un seul graphique. Rapport Medium importé ci-dessous. **[English version]({{< ref "/posts/multiple-indicators-backtesting/index.md" >}})**.

<!--more-->

## Installation des dépendances

Installez les bibliothèques nécessaires :

!pip install numpy httpx richp

## Imports

Modules à importer pour le script :

import pandas as pd  
import numpy as np  
from datetime import datetime  
import httpx  
import concurrent.futures  
import glob  
import warnings  
from rich.progress import track  
  
warnings.filterwarnings("ignore")

## Configuration API

Remplacez `FMP_API_KEY` et `BINANCE_API_KEY` par vos clés pour accéder aux services concernés.

BASE\_URL\_FMP = "https://financialmodelingprep.com/api/v3"  
BASE\_URL\_BINANCE = "https://fapi.binance.com/fapi/v1/"  
FMP\_API\_KEY = "YOUR\_FMP\_API\_KEY"  
BINANCE\_API\_KEY = "YOUR\_BINANCE\_API\_KEY"

## Fonctions de requêtes API

Ces fonctions appellent différents points de terminaison pour l’historique crypto et actions.

def make\_api\_request(api\_endpoint, params):  
    with httpx.Client() as client:  
        response = client.get(api\_endpoint, params=params)  
        if response.status\_code == 200:  
            return response.json()  
        print("Error: Failed to retrieve data from API")  
        return None  
  
def get\_historical\_price\_full\_crypto(symbol):  
    api\_endpoint = f"{BASE\_URL\_FMP}/historical-price-full/crypto/{symbol}"  
    params = {"apikey": FMP\_API\_KEY}  
    return make\_api\_request(api\_endpoint, params)  
  
def get\_historical\_price\_full\_stock(symbol):  
    api\_endpoint = f"{BASE\_URL\_FMP}/historical-price-full/{symbol}"  
    params = {"apikey": FMP\_API\_KEY}  
    return make\_api\_request(api\_endpoint, params)  
  
def get\_SP500():  
    api\_endpoint = "https://en.wikipedia.org/wiki/List\_of\_S%26P\_500\_companies"  
    data = pd.read\_html(api\_endpoint)  
    return list(data\[0\]\['Symbol'\])  
  
def get\_all\_crypto():  
    return \[  
        "BTCUSD", "ETHUSD", "LTCUSD", "BCHUSD", "XRPUSD", "EOSUSD",  
        "XLMUSD", "TRXUSD", "ETCUSD", "DASHUSD", "ZECUSD", "XTZUSD",  
        "XMRUSD", "ADAUSD", "NEOUSD", "XEMUSD", "VETUSD", "DOGEUSD",  
        "OMGUSD", "ZRXUSD", "BATUSD", "USDTUSD", "LINKUSD", "BTTUSD",  
        "BNBUSD", "ONTUSD", "QTUMUSD", "ALGOUSD", "ZILUSD", "ICXUSD",  
        "KNCUSD", "ZENUSD", "THETAUSD", "IOSTUSD", "ATOMUSD", "MKRUSD",  
        "COMPUSD", "YFIUSD", "SUSHIUSD", "SNXUSD", "UMAUSD", "BALUSD",  
        "AAVEUSD", "UNIUSD", "RENBTCUSD", "RENUSD", "CRVUSD", "SXPUSD",  
        "KSMUSD", "OXTUSD", "DGBUSD", "LRCUSD", "WAVESUSD", "NMRUSD",  
        "STORJUSD", "KAVAUSD", "RLCUSD", "BANDUSD", "SCUSD", "ENJUSD"  
    \]  
  
def get\_financial\_statements\_lists():  
    api\_endpoint = f"{BASE\_URL\_FMP}/financial-statement-symbol-lists"  
    params = {"apikey": FMP\_API\_KEY}  
    return make\_api\_request(api\_endpoint, params)

## Stratégie EMA

La **moyenne mobile exponentielle (EMA)** accorde plus de poids aux points récents ; elle réagit plus vite que la moyenne mobile simple (SMA).

class EMA(Strategy):  
    n1 = 20  
    n2 = 80  
  
    def init(self):  
        close = self.data.Close  
        self.ema20 = self.I(taPanda.ema, close.s, self.n1)  
        self.ema80 = self.I(taPanda.ema, close.s, self.n2)  
  
    def next(self):  
        price = self.data.Close  
        if crossover(self.ema20, self.ema80):  
            self.position.close()  
            self.buy(sl=0.90 \* price, tp=1.25 \* price)  
        elif crossover(self.ema80, self.ema20):  
            self.position.close()  
            self.sell(sl=1.10 \* price, tp=0.75 \* price)

Dans cette stratégie :

*   `ema20` et `ema80` sont calculées pour l’instrument.
*   Achat quand `ema20` croise au-dessus de `ema80`.
*   Vente quand `ema80` croise au-dessus de `ema20`.
*   Stop loss (`sl`) et take profit (`tp`) pour limiter les pertes et prendre des gains.

## Stratégie MACD

Le **MACD** est un indicateur de momentum qui compare deux moyennes mobiles (souvent EMA 12 et 26) ; la **ligne de signal** est une EMA 9 du MACD et sert de déclencheur d’achat/vente.

class MACD(Strategy):  
    short\_period = 12  
    long\_period = 26  
    signal\_period = 9  
  
    def init(self):  
        close = self.data.Close  
        self.macd = self.I(taPanda.macd, close.s, self.short\_period, self.long\_period, self.signal\_period)  
  
    def next(self):  
        macd\_line = self.macd.macd  
        signal\_line = self.macd.signal  
        if crossover(macd\_line, signal\_line):  
            self.position.close()  
            self.buy()  
        elif crossover(signal\_line, macd\_line):  
            self.position.close()  
            self.sell()

*   `macd_line` et `signal_line` dérivent des EMA courtes et longues.
*   Achat quand `macd_line` croise au-dessus de `signal_line`.
*   Vente quand `signal_line` croise au-dessus de `macd_line`.

## Exécuter les backtests

Fonctions pour traiter les instruments et lancer les stratégies choisies.

def run\_backtests\_strategies(instruments, strategies):  
    strategies = \[x for x in STRATEGIES if x.\_\_name\_\_ in strategies\]  
    outputs = \[\]  
    with concurrent.futures.ThreadPoolExecutor() as executor:  
        futures = \[\]  
        for strategy in strategies:  
            future = executor.submit(run\_backtests, instruments, strategy, 4)  
            futures.append(future)  
        for future in concurrent.futures.as\_completed(futures):  
            outputs.extend(future.result())  
    return outputs  
  
def check\_crypto(instrument):  
    return instrument in get\_all\_crypto()  
  
def check\_stock(instrument):  
    return instrument not in get\_financial\_statements\_lists()  
  
def process\_instrument(instrument, strategy):  
    try:  
        if check\_crypto(instrument):  
            data = get\_historical\_price\_full\_crypto(instrument)  
        else:  
            data = get\_historical\_price\_full\_stock(instrument)  
        if data is None or "historical" not in data:  
            print(f"Error processing {instrument}: No data")  
            return None  
        data = clean\_data(data)  
        bt = Backtest(data, strategy=strategy, cash=100000, commission=0.002, exclusive\_orders=True)  
        output = bt.run()  
        output = process\_output(output, instrument, strategy)  
        return output, bt  
    except Exception as e:  
        print(f"Error processing {instrument}: {str(e)}")  
        return None  
  
def clean\_data(data):  
    data = data\["historical"\]  
    data = pd.DataFrame(data)  
    data.columns = \[x.title() for x in data.columns\]  
    data = data.drop(\["Adjclose", "Unadjustedvolume", "Change", "Changepercent", "Vwap", "Label", "Changeovertime"\], axis=1)  
    data\["Date"\] = pd.to\_datetime(data\["Date"\])  
    data.set\_index("Date", inplace=True)  
    data = data.iloc\[::-1\]  
    return data  
  
def process\_output(output, instrument, strategy, in\_row=True):  
    if in\_row:  
        output = pd.DataFrame(output).T  
    output\["Instrument"\] = instrument  
    output\["Strategy"\] = strategy.\_\_name\_\_  
    output.pop("\_strategy")  
    return output  
  
def save\_output(output, output\_dir, instrument, start, end):  
    print(f"Saving output for {instrument}")  
    fileNameOutput = f"{output\_dir}/{instrument}-{start}-{end}.csv"  
    output.to\_csv(fileNameOutput)  
  
def plot\_results(bt, output\_dir, instrument, start, end):  
    print(f"Saving chart for {instrument}")  
    fileNameChart = f"{output\_dir}/{instrument}-{start}-{end}.html"  
    bt.plot(filename=fileNameChart, open\_browser=False)  
  
def run\_backtests(instruments, strategy, num\_threads=4, generate\_plots=False):  
    outputs = \[\]  
    output\_dir = f"output/raw/{strategy.\_\_name\_\_}"  
    output\_dir\_charts = f"output/charts/{strategy.\_\_name\_\_}"  
    if not os.path.exists(output\_dir):  
        os.makedirs(output\_dir)  
    if not os.path.exists(output\_dir\_charts):  
        os.makedirs(output\_dir\_charts)  
    with concurrent.futures.ThreadPoolExecutor(max\_workers=num\_threads) as executor:  
        future\_to\_instrument = {executor.submit(process\_instrument, instrument, strategy): instrument for instrument in instruments}  
        for future in concurrent.futures.as\_completed(future\_to\_instrument):  
            instrument = future\_to\_instrument\[future\]  
            output = future.result()  
            if output is not None:  
                outputs.append(output\[0\])  
                save\_output(output\[0\], output\_dir, instrument, output\[0\]\["Start"\].to\_string().strip().split()\[1\], output\[0\]\["End"\].to\_string().strip().split()\[1\])  
                if generate\_plots:  
                    plot\_results(output\[1\], output\_dir\_charts, instrument, output\[0\]\["Start"\].to\_string().strip().split()\[1\], output\[0\]\["End"\].to\_string().strip().split()\[1\])  
    data\_frame = pd.concat(outputs)  
    start = data\_frame\["Start"\].to\_string().strip().split()\[1\]  
    end = data\_frame\["End"\].to\_string().strip().split()\[1\]  
    fileNameOutput = f"output/{strategy.\_\_name\_\_}-{start}-{end}.csv"  
    data\_frame.to\_csv(fileNameOutput)  
    return data\_frame

## Lancer les scripts

tickers = get\_SP500()  
run\_backtests(tickers, strategy=EMA, num\_threads=12, generate\_plots=True)  
run\_backtests(tickers, strategy=MACD, num\_threads=12, generate\_plots=True)  
  
ticker = get\_all\_crypto()  
run\_backtests(ticker, strategy=EMA, num\_threads=12, generate\_plots=True)  
run\_backtests(ticker, strategy=MACD, num\_threads=12, generate\_plots=True)

Le dossier [output du dépôt BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting/tree/main/output) ne contient en général pas de résultats précalculés — les auteurs évitent d’y versionner des données spécifiques à chaque utilisateur.

Pour obtenir des chiffres, exécutez le script **localement** avec vos paramètres et stratégies ; les sorties iront dans le répertoire `output` du projet.

Exemple de graphique de référence : [EMA — AAPL](https://algoets.github.io/BatchBacktesting/output/charts/EMA/AAPL-2018-04-04-2023-04-03.html).

## Analyse des résultats

Exemple de classement EMA (rendements les plus hauts et plus bas) :

*   **Cinq instruments avec les rendements les plus élevés :**
*   BTCBUSD: 293.78%
*   ALB: 205.97%
*   OMGUSD: 199.62%
*   BBWI: 196.82%
*   GRMN: 193.47%
*   **Cinq instruments avec les rendements les plus faibles :**
*   BTTBUSD: -99.93%
*   UAL: -82.63%
*   NCLH: -81.51%
*   LNC: -78.02%
*   CHRW: -76.38%

![](./img-001.png)

## Bilan

Classer chaque symbole avec le même gabarit MACD/EMA aide l’**hygiène de recherche** (repérer des rendements absurdes, vérifier les APIs) — pas à déployer du capital. L’étape suivante reste la relecture manuelle des extrêmes, pas le trading automatique.

---

*Publié à l’origine sur [Medium](https://medium.com/@antoine.boucher012/multiple-technical-indicators-backtesting-on-multiple-tickers-using-python-a5c933d3f1bf).*
