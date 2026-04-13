---
post_kind: article
title: Expérimentation des indicateurs technique avec Python et Backtesting
date: 2024-05-14T20:00:00-04:00
tags:
    - Python
    - Backtesting
    - Trading
    - Français
canonicalURL: "https://medium.com/@antoine.boucher012/exp%C3%A9rimentation-des-indicateurs-technique-avec-python-et-backtesting-828bf93e92cc"
---

## Faites du Batch Backtesting sur les cryptos et les stocks

## Introduction

Dans ce rapport, nous présentons une expérimentation des indicateurs techniques à l’aide du projet BatchBacktesting disponible sur GitHub à l’adresse suivante :

[BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting/tree/main)

!pip install numpy httpx rich  
  
import pandas as pd  
import numpy as np  
from datetime import datetime  
import sys  
import os  
import httpx  
  
import concurrent.futures  
from datetime import datetime  
import glob  
import warnings  
from rich.progress import track  
warnings.filterwarnings("ignore")

## API

N’oubliez pas de remplacer les espaces réservés `FMP_API_KEY` et `BINANCE_API_KEY` par vos véritables clés API pour pouvoir accéder aux données des services respectifs.

BASE\_URL\_FMP = "https://financialmodelingprep.com/api/v3"  
BASE\_URL\_BINANCE = "https://fapi.binance.com/fapi/v1/"  
FMP\_API\_KEY = ""  
BINANCE\_API\_KEY = ""

Plusieurs fonctions pour effectuer des requêtes API et fournit une liste de cryptomonnaies prises en charge.

Ce script propose des fonctions pour :

1.  Effectuer des requêtes API vers différents points de terminaison.
2.  Obtenir des données historiques de prix pour les cryptomonnaies et les actions.
3.  Obtenir la liste des actions du S&P 500.
4.  Obtenir toutes les cryptomonnaies prises en charge.
5.  Obtenir les listes des états financiers.

def make\_api\_request(api\_endpoint, params):  
    with httpx.Client() as client:  
        \# Make the GET request to the API  
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
        "STORJUSD", "KAVAUSD", "RLCUSD", "BANDUSD", "SCUSD", "ENJUSD",  
    \]  
  
def get\_financial\_statements\_lists():  
    api\_endpoint = f"{BASE\_URL\_FMP}/financial-statement-symbol-lists"  
    params = {"apikey": FMP\_API\_KEY}  
    return make\_api\_request(api\_endpoint, params)  
    
def get\_Vanguard\_Canada():  
    """  
    Get Vanguard Canada companies  
    Returns:  
        dict: Dictionary containing the data  
    """  
        \# VCN: Vanguard FTSE Canada All Cap Index ETF  
        \# VFV: Vanguard S&P 500 Index ETF  
        \# VUN: Vanguard US Total Market Index ETF  
        \# VEE: Vanguard FTSE Emerging Markets All Cap Index ETF  
        \# VAB: Vanguard Canadian Aggregate Bond Index ETF  
        \# VSB: Vanguard Canadian Short-Term Bond Index ETF  
        \# VXC: Vanguard FTSE Global All Cap ex Canada Index ETF  
        \# VIU: Vanguard FTSE Developed All Cap ex North America Index ETF  
        \# VGG: Vanguard US Dividend Appreciation Index ETF  
    return \['VCN', 'VFV', 'VUN', 'VEE', 'VAB', 'VSB', 'VXC', 'VIU', 'VGG'\]  

Pour utiliser ce script dans votre projet, copiez simplement assurez-vous d’avoir installé les bibliothèques requises mentionnées dans la section “Exigences” de la documentation BatchBacktesting. Ensuite, vous pouvez importer les fonctions de ce script dans votre script principal ou votre Jupyter Notebook pour accéder et manipuler les données comme vous le souhaitez.

## Get Antoine Boucher’s stories in your inbox

Une fois que vous avez les données, vous pouvez utiliser la bibliothèque BatchBacktesting pour tester diverses stratégies sur les actions ou les cryptomonnaies, analyser les résultats et visualiser les performances. À titre d’exemple, nous avons utilisé la stratégie EMA (Exponential Moving Average) pour effectuer des tests de performance sur les actions du S&P 500 et les cryptomonnaies prises en charge.

## EMA Stratégie

L’EMA est un indicateur technique qui est utilisé pour lisser l’action des prix en filtrant le “bruit” des fluctuations de prix aléatoires à court terme. Il est calculé en prenant le prix moyen d’un titre sur un nombre spécifique de périodes de temps. L’EMA est un type de moyenne mobile qui accorde un poids et une signification plus importants aux points de données les plus récents. La moyenne mobile exponentielle est également appelée moyenne mobile pondérée exponentiellement.

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

def run\_backtests\_strategies(instruments, strategies):  
    """  
    Run backtests for a list of instruments using a specified strategy.Args:  
        instruments (list): List of instruments to run backtests for  
        strategies (list): List of strategies to run backtests for  
    Returns:  
        List of outputs from run\_backtests()  
    """  
    \# find strategies in the STRATEGIES  
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
    """  
    Check if the instrument is crypto or not  
    """  
    return instrument in get\_all\_crypto()  
  
def check\_stock(instrument):  
    """  
    Check if the instrument is crypto or not  
    """  
    return instrument not in get\_financial\_statements\_lists()  
  
def process\_instrument(instrument, strategy):  
    """  
    Process a single instrument for a backtest using a specified strategy.  
    Returns a Pandas dataframe of the backtest results.  
    """  
    try:  
        if check\_crypto(instrument):  
            data = get\_historical\_price\_full\_crypto(instrument)  
        else:  
            data = get\_historical\_price\_full\_stock(instrument)  
        if data is None or "historical" not in data:  
            print(f"Error processing {instrument}: No data")  
            return None  
        data = clean\_data(data)  
        bt = Backtest(  
            data, strategy=strategy, cash=100000, commission=0.002, exclusive\_orders=True  
        )  
        output = bt.run()  
        output = process\_output(output, instrument, strategy)  
        return output, bt  
    except Exception as e:  
        print(f"Error processing {instrument}: {str(e)}")  
        return None  
  
def clean\_data(data):  
    """  
    Clean historical price data for use in a backtest.  
    Returns a Pandas dataframe of the cleaned data.  
    """  
    data = data\["historical"\]  
    data = pd.DataFrame(data)  
    data.columns = \[x.title() for x in data.columns\]  
    data = data.drop(  
        \[  
            "Adjclose",  
            "Unadjustedvolume",  
            "Change",  
            "Changepercent",  
            "Vwap",  
            "Label",  
            "Changeovertime",  
        \],  
        axis=1,  
    )  
    data\["Date"\] = pd.to\_datetime(data\["Date"\])  
    data.set\_index("Date", inplace=True)  
    data = data.iloc\[::-1\]  
    return data  
  
def process\_output(output, instrument, strategy, in\_row=True):  
    """  
    Process backtest output data to include instrument name, strategy name,  
    and parameters.  
    Returns a Pandas dataframe of the processed output.  
    """  
    if in\_row:  
        output = pd.DataFrame(output).T  
    output\["Instrument"\] = instrument  
    output\["Strategy"\] = strategy.\_\_name\_\_  
    output.pop("\_strategy")  
    return output  
  
def save\_output(output, output\_dir, instrument, start, end):  
    """  
    Save backtest output to file and generate chart if specified.  
    """  
    print(f"Saving output for {instrument}")  
    fileNameOutput = f"{output\_dir}/{instrument}\-{start}\-{end}.csv"  
    output.to\_csv(fileNameOutput)  
  
def plot\_results(bt, output\_dir, instrument, start, end):  
    print(f"Saving chart for {instrument}")  
    fileNameChart = f"{output\_dir}/{instrument}\-{start}\-{end}.html"  
    bt.plot(filename=fileNameChart, open\_browser=False)  
def run\_backtests(instruments, strategy, num\_threads=4, generate\_plots=False):  
    """  
    Run backtests for a list of instruments using a specified strategy.  
    Returns a list of Pandas dataframes of the backtest results.  
    Args:  
        instruments (list): List of instruments to run backtests for  
    Returns:  
        List of Pandas dataframes of the backtest results  
    """  
    outputs = \[\]  
    output\_dir = f"output/raw/{strategy.\_\_name\_\_}"  
    output\_dir\_charts = f"output/charts/{strategy.\_\_name\_\_}"  
    if not os.path.exists(output\_dir):  
        os.makedirs(output\_dir)  
    if not os.path.exists(output\_dir\_charts):  
        os.makedirs(output\_dir\_charts)  
    with concurrent.futures.ThreadPoolExecutor(max\_workers=num\_threads) as executor:  
        future\_to\_instrument = {  
            executor.submit(process\_instrument, instrument, strategy): instrument  
            for instrument in instruments  
        }  
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
    fileNameOutput = f"output/{strategy.\_\_name\_\_}\-{start}\-{end}.csv"  
    data\_frame.to\_csv(fileNameOutput)  
  
    return data\_frame  

Le script génère des graphiques pour chaque instrument testé, qui peuvent être visualisés pour analyser les performances des stratégies appliquées. Les résultats sont sauvegardés dans le répertoire `output` du projet BatchBacktesting.

tickers \= get\_SP500()  
run\_backtests(tickers, strategy\=EMA, num\_threads\=12, generate\_plots\=True)  
ticker \= get\_all\_crypto()  
run\_backtests(ticker, strategy\=EMA, num\_threads\=12, generate\_plots\=True)

Le lien que vous avez partagé correspond au répertoire `output` du projet BatchBacktesting sur GitHub : [https://github.com/AlgoETS/BatchBacktesting/tree/main/output](https://github.com/AlgoETS/BatchBacktesting/tree/main/output). Cependant, il semble que ce répertoire ne contient pas de résultats pré-calculés. En effet, il est probable que les auteurs du projet aient choisi de ne pas inclure les résultats des tests dans le dépôt GitHub afin d'éviter d'encombrer le dépôt avec des données spécifiques à chaque utilisateur.

Pour obtenir des valeurs calculées pour vos propres tests, vous devrez exécuter le script en local sur votre machine avec les paramètres et les stratégies de votre choix. Après avoir exécuté le script, les résultats seront sauvegardés dans le répertoire `output` de votre projet local.

[https://algoets.github.io/BatchBacktesting/output/charts/EMA/AAPL-2018-04-04-2023-04-03.html](https://algoets.github.io/BatchBacktesting/output/charts/EMA/AAPL-2018-04-04-2023-04-03.html)

## Analyse

Top 5 des instruments avec le meilleur rendement :

1.  BTCBUSD : 293,78%
2.  ALB : 205,97%
3.  OMGUSD : 199,62%
4.  BBWI : 196,82%
5.  GRMN : 193,47%

Top 5 des instruments avec le plus faible rendement :

1.  BTTBUSD : -99,93%
2.  UAL : -82,63%
3.  NCLH : -81,51%
4.  LNC : -78,02%
5.  CHRW : -76,38%

Press enter or click to view image in full size

![](./img-001.png)

En conclusion, le projet BatchBacktesting offre une approche flexible et puissante pour tester et analyser les performances des indicateurs techniques sur les marchés boursiers et les cryptomonnaies. Les fonctions fournies permettent une intégration facile avec les API de services financiers et une manipulation aisée des données. Les résultats des expérimentations peuvent être utilisés pour développer et affiner des stratégies de trading algorithmique en fonction des performances observées.

---

*Publié originalement sur [Medium](https://medium.com/@antoine.boucher012/exp%C3%A9rimentation-des-indicateurs-technique-avec-python-et-backtesting-828bf93e92cc).*
