# Renpho scale, Home Assistant, reverse-engineering the API, and a weight forecast

> Forking hass_renpho for Home Assistant — old Renpho app API, APKLeaks, Lovelace dashboards, proxy quirks, a pandas + LSTM notebook that forecasts weight from the export, and habits that keep bio-impedance useful.

- HTML page: https://antoineboucher.info/CV/blog/posts/renpho-health-api-blueprint/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/posts/renpho-health-api-blueprint/index.md
- Published: 2021-10-10
- Updated: 2026-11-05
- Tags: Health, API, Reverse Engineering, Home Assistant, Home Automation
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)I wanted scale readings in **Home Assistant** next to the rest of my apartment automations — not another siloed health app. That turned into maintaining **[hass_renpho](https://github.com/antoinebou12/hass_renpho)** (a fork of the quiet community integration), running **APKLeaks** on the Android client, a Lovelace board I still open when training or sleep changes, and a notebook that tries to forecast weight from the exported history.

## Why not only the Renpho app

A **Renpho** scale with bio-impedance spits out more than weight — BMI, BMR, body age, fat and muscle estimates, water, protein, visceral-fat indices, and a pile of resistance fields per limb if you pull the full payload. Useful only if the numbers live where you already look: history graphs, automations, and the same **[homelab](https://antoineboucher.info/CV/blog/posts/home-networking-evolution/)** mindset as everything else self-hosted at home.

## Inspiration (without the cult)

Personal tracking, for me, started around the same time people were talking about Bryan Johnson’s **“Blueprint”** push for self-quantification. I am not selling a protocol — the point was simpler: **trends over time**, same conditions, don’t panic on one morning spike. The photo below is mood board energy, not medical advice.

![Self-quantification mood board — inspiration for tracking habits, not a product endorsement](https://antoineboucher.info/CV/blog/posts/renpho-health-api-blueprint/images/blueprint.jpg)

## Where hass_renpho came from

Neil Allen’s write-ups — [reverse-engineering the Renpho app](https://neilgaryallen.dev/blog/reverse-engineering-the-renpho-app) and [Renpho → Home Assistant](https://neilgaryallen.dev/blog/renpho-to-home-assistant) — did the hard thinking first. The community repo **[neilzilla/hass-renpho](https://github.com/neilzilla/hass-renpho)** wrapped that into a Home Assistant custom component.

When activity slowed and I needed more entities exposed, I forked to **[antoinebou12/hass_renpho](https://github.com/antoinebou12/hass_renpho)**. The README is honest about constraints:

> This integration targets the **older Renpho app** cloud API. Newer app versions may not work; treat it as a hobby integration, not a supported product.

There is a small **API explorer** at [hass-renpho.vercel.app/docs](https://hass-renpho.vercel.app/docs) if you want to poke the JSON with your own credentials before touching HA.

### What the fork actually does

- Logs into Renpho’s cloud (`renpho.qnclouds.com`) with email/password (same as the phone app).
- Polls on a **`refresh`** interval you set in YAML or the UI.
- Exposes **sensors** for weight, composition, metabolic estimates, device metadata, and optional girth/goals when the account has them.
- Optional **`proxy`** URL when your home IP is throttled or blocked but the app works on cellular data.

I kept talking with the original maintainer when it made sense — share payload shapes, avoid duplicate fixes, keep one integration useful for anyone else with a scale in the closet.

## Install path I used

1. **[HACS](https://hacs.xyz/)** on Home Assistant (or copy `custom_components/renpho` from the repo).
2. Drop credentials in **`configuration.yaml`** (legacy platform style in my fork):

```yaml
renpho:
  email: you@example.com
  password: !secret renpho_password
  refresh: 600  # seconds between polls — logging in here can log you out of the app
  # proxy: http://127.0.0.1:8080  # optional — only this integration’s traffic

sensor:
  - platform: renpho
```

3. Restart HA, confirm entities appear, then build Lovelace.

**Heads-up:** polling logs you into the cloud API; Renpho may kick your phone session. I picked a **600s** refresh so I was not hammering login on every automation tick.

## Metrics the integration surfaces

The fork documents dozens of fields. In practice I watch a smaller set in Lovelace; the rest are there if you automate or debug.

| Group | Examples | Units |
|-------|----------|-------|
| **Core** | weight, BMI, body fat, water, muscle, bone | kg, % |
| **Shape** | waistline, hip, stature | cm |
| **Metabolic** | BMR, protein | kcal/day, % |
| **Age** | body age | years |
| **Visceral / subcutaneous** | visfat, subfat | level, % |
| **Device** | scale name, MAC, model, timezone | strings |
| **Bio-impedance raw** | resistance per limb (20 kHz / 100 kHz style fields) | ohms |

Full tables live in the **[repo README](https://github.com/antoinebou12/hass_renpho#supported-metrics)** — handy when APKLeaks shows a new key and you need a matching sensor.

The raw measurement records behind those sensors carry more than the table. Each weigh-in in my export has segment fields (`bodyfat_*` and `sinew_*` for each arm, each leg and the trunk), separate `left_weight` / `right_weight`, two sets of per-segment resistances named `resistance20_*` and `resistance100_*`, plus `heart_rate`, `cardiac_index`, `body_shape` and a `score`. Girth comes from a separate list with one `*_value` / `*_unit` pair per site (neck, shoulder, chest, waist, abdomen, hip, arm, thigh, calf, left and right variants, waist-to-hip ratio) and a few custom slots. Goals are a third list: one record per girth type with initial, goal and finish values and their timestamps.

## When the cloud API fights your network

Residential or datacenter egress sometimes fails against Renpho’s cloud even when the official app works on LTE. Symptoms: auth errors, empty lists, random HTTP failures in HA logs.

Mitigations from the README:

1. **VPN on the HA host** — change egress IP for everything on that machine.
2. **`proxy` in config** — only Renpho traffic goes through your HTTP/SOCKS proxy (credentials pass through that path — use something you trust).

I document this because it burned an evening that looked like “broken integration” but was really **IP reputation**.

## Reverse engineering with APKLeaks

Renpho does not ship a public API PDF. Next step: see what the **Android APK** calls.

**[APKLeaks](https://github.com/dwisiswant0/apkleaks)** scans the package for strings — hosts, paths, keys — without a full decompile session:

```bash
pip install apkleaks
git clone https://github.com/dwisiswant0/apkleaks
cd apkleaks && pip install -r requirements.txt
apkleaks -f /path/to/renpho.apk -o renpho-leaks.txt
```

I matched leaked URLs and parameter names to the JSON fields the integration already mapped, then filled gaps when Lovelace showed `unknown` for a new key after an app update.

Further reading:

- [APKLeaks on GitHub](https://github.com/dwisiswant0/apkleaks)
- [White Oak Security — APKLeaks overview](https://www.whiteoaksecurity.com/blog/apkleaks-discover-leaks-within-apk-files/)

Treat anything you extract as an **unstable contract** — store updates break custom integrations; that is the hobby tax.

## Lovelace dashboards

Two views I actually use: vitals + history, then girth/goals when Renpho syncs them.

![Home Assistant Lovelace — Renpho weight history, body-composition gauges, and supporting entity rows](https://antoineboucher.info/CV/blog/posts/renpho-health-api-blueprint/images/lovelace-metrics.png)

Weight trend at the top, composition gauges in the middle, “extra” metrics as entities you can hide if they noise you out.

![Home Assistant Lovelace — Renpho girth measurements and body goals from the cloud account](https://antoineboucher.info/CV/blog/posts/renpho-health-api-blueprint/images/lovelace-girth.png)

Girth and goals only matter if your Renpho profile has them; otherwise this panel stays empty and that is fine.

## Forecasting weight from the export

Once the history was out of the app, I wanted to see what a model would make of it. The notebook is plain **pandas**, **scikit-learn**, **TensorFlow/Keras** and **keras-tuner**. It models **weight only**: the girth and goal lists are loaded but never used as features.

### Preparing the series

1. Save the raw JSON lists returned by the API (measurements, girth, girth goals) to local files and load the measurements into a DataFrame.
2. Keep one user ID. Records carry a per-user ID, so a shared scale does not mix people.
3. Parse `created_at` (a string with a UTC offset), sort by it, drop the timezone to avoid mismatches when comparing and plotting dates, and add an ordinal date column for the regression baselines.

### Two baselines

- **Linear regression** on the ordinal date: a trend line extended 30 days past the last reading, with the next-day and +30-day values highlighted on the plot.
- **Random forest** (100 trees) on degree-2 polynomial features of the date, with a daily prediction curve for the following month.

Both use `train_test_split` with a random shuffle, which is the wrong split for a time series (see the limits below).

### The LSTM

Weights are scaled to 0–1 with `MinMaxScaler`, then cut into sliding windows: the previous `look_back` readings are the input, the next reading is the target.

```python
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back - 1):
        X.append(dataset[i:(i + look_back), 0])
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

X, Y = create_dataset(scaled_weights, look_back=30)
X = np.reshape(X, (X.shape[0], 1, X.shape[1]))   # (samples, 1 timestep, 30 features)
```

The first model is small on purpose: `LSTM(4)` then `Dense(1)`, mean squared error, Adam, batch size 1, up to 100 epochs with early stopping on the training loss (patience 2). The split is chronological this time, the first 67% for training and the rest for testing. Predictions are scaled back to kilograms before computing train and test RMSE.

The second pass widens the window to 60 readings and lets **keras-tuner** pick the number of units and the learning rate:

```python
def build_model(hp):
    model = Sequential()
    model.add(LSTM(units=hp.Int('units', min_value=4, max_value=64, step=4),
                   input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error',
                  optimizer=Adam(hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])))
    return model

tuner = kt.RandomSearch(build_model, objective='val_loss',
                        max_trials=5, executions_per_trial=3)
```

Five trials ran, each averaged over three executions, with early stopping on validation loss (patience 5). The best configuration was 52 units at a learning rate of 1e-3, and the only trial at 1e-4 scored worst. The winning model is rebuilt, refit, and then rolled forward one step at a time for 365 steps: each prediction is appended to the window and the oldest value drops off.

### Limits I would fix today

- **Random splits on a time series.** The linear and random-forest baselines shuffle dates, so the test set sits between training points. Use a chronological split or `TimeSeriesSplit` (imported in the notebook, never used).
- **Trees do not extrapolate.** A random forest predicts averages of training targets, so past the last date its “forecast” is a flat line. Polynomial features of a single date do not change that.
- **Steps are weigh-ins, not days.** A window of 30 is the last 30 readings, whatever days they fell on, yet the forecast is plotted one step per day. Resample to a daily series first.
- **The LSTM never sees a sequence.** With input shape `(1, look_back)` the window is one timestep with 30 or 60 features, so the recurrence does nothing. `(look_back, 1)` is the shape that makes it read the window in order.
- **Scaler fitted before the split**, and the tuner uses the test set as its validation set, so no data is left that the model selection never touched.
- **A 365-step recursive forecast compounds its own errors.** Past a few weeks, read it as a shape, not a number.

None of this replaces the habits table below: consistent weigh-ins matter more to the curve than the model on top of it.

## Context outside HA

Renpho is one input. I still mirror activity and food elsewhere (**Google Health**, **MyFitnessPal**) so scale readings sit next to movement and calories, not alone in a vacuum.

### Habits that kept the series usable

| Habit | Why |
|-------|-----|
| **Same time of day** | Mornings, similar hydration — otherwise you are comparing apples to soup |
| **Clothing constant** | ~1 kg swing is normal noise, not “fat overnight” |
| **Trends over weeks** | Bio-impedance composition lags reality; react to slopes |
| **Hide gauges you ignore** | If you do not act on visceral fat %, remove the card |

This started as a technical side project and became a steady habit: enough signal to notice when training or sleep changes show up in weight and energy, not enough precision for clinic decisions.

## When not to do this

- You need **clinical** body composition — consumer scales estimate, they do not diagnose.
- You cannot run the **legacy app/API** path the integration expects.
- You will not maintain a fork when Renpho changes the app — budget breakage.
- Daily fat % will ruin your mood — curate the dashboard ruthlessly.
- You plan to share exports. A raw measurement record carries birthday, gender, height, a user ID and the scale’s MAC address next to the body values; strip those before anything leaves your machine.

## Repo links (quick)

| Resource | URL |
|----------|-----|
| My fork | [github.com/antoinebou12/hass_renpho](https://github.com/antoinebou12/hass_renpho) |
| Upstream lineage | [github.com/neilzilla/hass-renpho](https://github.com/neilzilla/hass-renpho) |
| API docs / playground | [hass-renpho.vercel.app/docs](https://hass-renpho.vercel.app/docs) |
| Original RE blog | [neilgaryallen.dev — Renpho series](https://neilgaryallen.dev/blog/reverse-engineering-the-renpho-app) |

## Related posts

- [Home networking evolution](https://antoineboucher.info/CV/blog/posts/home-networking-evolution/) — same “own your infra” thread
- [MediaBox homelab notes](https://antoineboucher.info/CV/blog/posts/mediabox-homelab-docker-catalog/) — another self-hosted stack at home
- [Economics of LEGO with data science](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/) — another dataset curiosity project

If you self-host health data, what actually stuck — Home Assistant, Grafana, or phone-only apps? The gadget is rarely the hard part; fitting the routine is.
