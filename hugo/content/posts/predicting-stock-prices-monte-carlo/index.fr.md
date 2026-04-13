---
post_kind: article
title: "Prévoir des cours boursiers avec des simulations Monte Carlo"
date: 2024-05-14T09:00:00-04:00
description: Simulation de trajectoires Monte Carlo en Python à partir de rendements historiques — bandes de risque, quantiles et comparaison à une période de validation.
translationKey: predicting-stock-prices-monte-carlo
tags:
    - Python
    - Finance
    - Monte Carlo
    - Backtesting
canonicalURL: "https://medium.com/@antoine.boucher012/predicting-stock-prices-with-monte-carlo-simulations-0884ef32c35b"
---

## Introduction

En finance, on raisonne rarement sur un seul prix « prévu » : il s’agit plutôt de **fourchettes**, de **risque de queue** et de **mesurer à quel point** les modèles simples peuvent se tromper. Cet article déroule une **simulation Monte Carlo de trajectoires** en Python : on estime dérive et volatilité à partir des clôtures historiques, on simule de nombreux chemins de prix futurs (pas discret façon brownien géométrique), et on résume le tout par une **distribution** — l’objet adapté aux questions de risque (bandes, quantiles, recouvrement par rapport à une période tenue hors échantillon).

Le **Monte Carlo par chaînes de Markov (MCMC)**, comme dans l’article de Landauskas et Valakevičius sur la modélisation des cours, est un autre outil : il **tire des échantillons** d’une loi qui n’a pas à être gaussienne simple — par exemple construite par **estimation par noyau** des prix observés — alors que le code ci-dessous suppose des chocs log-normaux à partir de dérive et volatilité estimées. Un flux pratique est **MCMC (ou autre inférence) pour la loi des données**, puis **Monte Carlo forward** pour les scénarios multi-périodes. Ce billet implémente explicitement le pas GBM forward ; voir les références et le lien WIP ci-dessous pour aller vers du MCMC « papier ».

## Étape 1 : environnement Python

Installez les bibliothèques nécessaires (`pandas`, `numpy`, `httpx`, `backtesting`, `pandas_ta`, `matplotlib`, `scipy`, `rich`, etc.) :

import pandas as pd  
import numpy as np  
from datetime import datetime  
import concurrent.futures  
import warnings  
from rich.progress import track  
from backtesting import Backtest, Strategy  
import pandas\_ta as ta  
import matplotlib.pyplot as plt  
from scipy.stats import norm  
import httpx  
  
warnings.filterwarnings("ignore")

## Étape 2 : fonctions utilitaires

Fonctions pour récupérer l’historique actions et crypto via API :

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

## Étape 3 : séparer entraînement et test

On récupère l’historique pour un symbole et on garde **deux** jeux : **avant** janvier 2023 (estimation du modèle et simulations) et **à partir de** janvier 2023 (hors échantillon pour comparer les plages simulées aux prix réalisés).

stock\_symbol = "AAPL"  
stock\_prices = get\_historical\_price\_full\_stock(stock\_symbol)  
data = pd.DataFrame(stock\_prices\['historical'\])  
  
def prepare\_price\_frame(df):  
    df = df.rename(columns={  
        'open': 'Open',  
        'high': 'High',  
        'low': 'Low',  
        'close': 'Close',  
        'volume': 'Volume',  
    })  
    required\_columns = \['date', 'Open', 'High', 'Low', 'Close', 'Volume'\]  
    return df\[required\_columns\].sort\_values(by=\['date'\], ascending=True).reset\_index(drop=True)  
  
prices\_before\_january\_2023 = prepare\_price\_frame(data\[data\['date'\] < '2023-01-01'\])  
prices\_after\_january\_2023 = prepare\_price\_frame(data\[data\['date'\] >= '2023-01-01'\])  

plt.figure(figsize=(10, 6))  
plt.title('Stock Prices')  
plt.xlabel('Date')  
plt.ylabel('Price')  
plt.plot(prices\_before\_january\_2023\['date'\], prices\_before\_january\_2023\['Close'\], label='Train (before Jan 2023)')  
plt.plot(prices\_after\_january\_2023\['date'\], prices\_after\_january\_2023\['Close'\], label='Hold-out (from Jan 2023)')  
plt.legend()  
plt.show()

![](./img-001.png)

![](./img-002.png)

## Étape 4 : simulation Monte Carlo (trajectoires forward et bandes de risque)

La fonction ci-dessous est une **simulation Monte Carlo** d’un modèle à **paramètres constants** : on estime moyenne et variance des **rendements logarithmiques** sur la fenêtre d’entraînement, on construit une **dérive** et une **volatilité** journalières, puis on tire de nombreux chocs gaussiens indépendants et on propage le prix vers l’avant. Ce n’est **pas** du MCMC ; il n’y a pas ici d’échantillonnage d’une loi a posteriori par chaîne de Markov. C’est le type de moteur de **scénarios forward** qu’on lance souvent **après** une étape d’inférence. À l’inverse, [Landauskas et Valakevičius (*Intellectual Economics*, 2011)](https://ojs.mruni.eu/ojs/intellectual-economics/article/view/817) utilisent le **MCMC pour échantillonner** une loi façonnée par une **estimation par noyau** des prix (propositions linéaires par morceaux). Notre raccourci GBM est plus simple ; l’article est la référence pour l’étape d’échantillonnage proche des données.

Pour un travail en cours sur cette ligne (expériences batch, vues de risque plus riches, rapprochement d’un MCMC « papier »), voir cette [expérimentation LinkedIn (WIP)](https://lnkd.in/eTUeTsAS).

Les sorties utiles pour le risque sont des **distributions** : quantiles du prix terminal, **bandes** façon prédiction (par ex. chemins 5e–95e percentile), et contrôles de **recouvrement** sur l’hors échantillon (le prix réalisé tombait-il là où la masse simulée était ?).

def monte\_carlo\_simulation(data, days, iterations):  
    if isinstance(data, pd.Series):  
        data = data.to\_numpy()  
    if not isinstance(data, np.ndarray):  
        raise TypeError("Data must be a numpy array or pandas Series")  
  
    log\_returns = np.log(data\[1:\] / data\[:-1\])  
    mean = np.mean(log\_returns)  
    variance = np.var(log\_returns)  
    drift = mean - (0.5 \* variance)  
    daily\_volatility = np.std(log\_returns)  
  
    future\_prices = np.zeros((days, iterations))  
    current\_price = data\[-1\]  
    for t in range(days):  
        shocks = drift + daily\_volatility \* norm.ppf(np.random.rand(iterations))  
        future\_prices\[t\] = current\_price \* np.exp(shocks)  
        current\_price = future\_prices\[t\]  
    return future\_prices

![](./img-003.png)

![](./img-004.png)

## Visualisation

simulation\_days = 364  
mc\_iterations = 1000  
mc\_prices = monte\_carlo\_simulation(prices\_before\_january\_2023\['Close'\], simulation\_days, mc\_iterations)  
  
last\_train\_close = prices\_before\_january\_2023\['Close'\].iloc\[-1\]  
last\_close\_price = np.full((1, mc\_iterations), last\_train\_close)  
mc\_prices\_combined = np.concatenate((last\_close\_price, mc\_prices), axis=0)  
  
last\_date = prices\_before\_january\_2023\['date'\].iloc\[-1\]  
simulated\_dates = pd.date\_range(start=last\_date, periods=simulation\_days + 1)  
  
\# Percentiles across paths at each future step (risk band)  
p05 = np.percentile(mc\_prices\_combined, 5, axis=1)  
p50 = np.percentile(mc\_prices\_combined, 50, axis=1)  
p95 = np.percentile(mc\_prices\_combined, 95, axis=1)  
mean\_path = mc\_prices\_combined.mean(axis=1)  
  
\# Terminal distribution at the last simulated step (VaR-style summaries)  
terminal\_prices = mc\_prices\_combined\[simulation\_days, :]  
mean\_terminal\_price = float(np.mean(terminal\_prices))  
q5, q50, q95 = np.percentile(terminal\_prices, \[5, 50, 95\])  
terminal\_return = terminal\_prices / last\_train\_close - 1.0  
ret\_q5, ret\_q50, ret\_q95 = np.percentile(terminal\_return, \[5, 50, 95\])  
  
horizon\_idx = min(simulation\_days, len(prices\_after\_january\_2023) - 1)  
real\_price = float(prices\_after\_january\_2023\['Close'\].iloc\[horizon\_idx\])  
real\_date = prices\_after\_january\_2023\['date'\].iloc\[horizon\_idx\]  
in\_90\_band = q5 <= real\_price <= q95  
  
print(f"Simulated horizon: {simulation\_days} trading days after {last\_date}")  
print(f"Mean terminal price: ${mean\_terminal\_price:.2f}")  
print(f"Terminal price percentiles (5 / 50 / 95): ${q5:.2f} / ${q50:.2f} / ${q95:.2f}")  
print(f"Terminal simple return vs last train close — 5th / 50th / 95th %ile: {ret\_q5\*100:.2f}% / {ret\_q50\*100:.2f}% / {ret\_q95\*100:.2f}%")  
print(f"Hold-out price at aligned step ({real\_date}): ${real\_price:.2f}")  
print(f"Realized price inside simulated 5–95% band: {in\_90\_band}")  
  
plt.figure(figsize=(10, 6))  
for i in range(mc\_iterations):  
    plt.plot(simulated\_dates, mc\_prices\_combined\[:, i\], linewidth=0.5, color='gray', alpha=0.02)  
plt.fill\_between(simulated\_dates, p05, p95, alpha=0.25, label='5th–95th percentile band')  
plt.plot(simulated\_dates, p50, label='Median path', linewidth=2, color='C0')  
plt.plot(simulated\_dates, mean\_path, label='Mean path', linewidth=2, linestyle='--', color='C1')  
plt.plot(pd.to\_datetime(prices\_before\_january\_2023\['date'\]), prices\_before\_january\_2023\['Close'\], label='Train (before Jan 2023)', linewidth=2, color='black')  
plt.plot(pd.to\_datetime(prices\_after\_january\_2023\['date'\]), prices\_after\_january\_2023\['Close'\], label='Hold-out (from Jan 2023)', linewidth=2, color='green')  
plt.axvline(pd.to\_datetime(real\_date), color='red', linestyle=':', linewidth=1, alpha=0.8, label='Hold-out step aligned to horizon')  
plt.scatter(\[pd.to\_datetime(real\_date)\], \[real\_price\], color='red', s=40, zorder=5, label='Realized (aligned)')  
  
plt.title('Monte Carlo Simulation of Stock Prices (with percentile band)')  
plt.xlabel('Date')  
plt.ylabel('Price')  
plt.legend(loc='upper left', fontsize=8)  
plt.show()

![](./img-005.png)

![](./img-006.png)

![](./img-007.png)

![](./img-008.png)

## Conclusion

Le **Monte Carlo forward** fournit une **distribution** de prix futurs sous une dynamique supposée — adapté aux **bandes de quantiles**, au comportement de **queue** et aux contrôles de **recouverture** sur données hors échantillon. C’est une étape distincte du **MCMC**, qui sert à **échantillonner** sous un modèle flexible des données (comme l’approche KDE de Landauskas et Valakevičius) avant ou en parallèle de la simulation forward. Pipeline typique : **ajuster ou échantillonner la loi qui colle à l’historique**, puis **faire avancer les scénarios par Monte Carlo**. Avec du **backtest** de stratégie, on sépare « à quel point le risque de modèle est large ? » de « une règle est-elle rentable ? »

Code d’exploration lié : [AlgoETS/MarkokChainMonteCarlo](https://github.com/AlgoETS/MarkokChainMonteCarlo) (expériences MCMC / stratification).

## Références

*   Landauskas, M. & Valakevičius, E. (2011). [*Modelling of Stock Prices by Markov Chain Monte Carlo Method*](https://ojs.mruni.eu/ojs/intellectual-economics/article/view/817) — *Intellectual Economics*, Vol. 5 No. 2 (article page); [PDF download](https://ojs.mruni.eu/ojs/intellectual-economics/article/download/817/774/1511).
*   [Semantic Scholar index](https://www.semanticscholar.org/paper/MODELLING-OF-STOCK-PRICES-BY-THE-MARKOV-CHAIN-MONTE-Landauskas-Valakevi%C4%8Dius/ced26fa31b2306e747d69de10b77aaf3b9704e7a) for the same paper.
*   [Neural Networks in Finance: Markov Chain Monte Carlo (MCMC) and Stochastic Volatility Modeling](/analytics-vidhya/neural-networks-in-finance-markov-chain-monte-carlo-mcmc-and-stochastic-volatility-modelling-3f4f148c3046)
*   [Monte Carlo Simulation Basics](https://www.investopedia.com/articles/investing/112514/monte-carlo-simulation-basics.asp)

---

*Publié à l’origine sur [Medium](https://medium.com/@antoine.boucher012/predicting-stock-prices-with-monte-carlo-simulations-0884ef32c35b).*
