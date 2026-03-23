# 📊 Schema KPI per analisi stile Aimchess

Questo documento descrive i principali KPI da estrarre da un dataset di partite di scacchi, includendo tempo speso, classificazione mosse e fase di gioco. Può essere usato come guida per elaborazioni future.

---

## 1️⃣ Accuracy e qualità delle mosse

**Obiettivo:** capire quanto un giocatore prende decisioni corrette e quanto il tempo influisce sulle scelte.

| KPI | Formula / Metodo | Note |
|-----|-----------------|------|
| **Accuracy totale** | media pesata delle mosse: <br>`accuracy_player = Σ(accuracy_mossa ⋅ weight_mossa) / Σ(weight_mossa)` | weight_mossa può essere 1 o basata sul tempo |
| **Accuracy pesata col tempo** | `weight_mossa = t_speso / t_total` o `weight_mossa = log(1 + t_speso)` <br>poi `accuracy = Σ(accuracy ⋅ weight) / Σ(weight)` | penalizza o premia mosse fatte con più tempo |
| **Accuracy per fase di gioco** | calcola separatamente per **apertura, mediogioco, finale** | consente insight su punti di forza/debolezza |
| **Best/Splendid/Perfect moves %** | `# Best / # mosse totali` | KPI qualitativi già classificati |

---

## 2️⃣ Tempo speso e pressione

**Obiettivo:** misurare la pressione temporale e il suo effetto sulle mosse.

| KPI | Formula / Metodo | Note |
|-----|-----------------|------|
| **Pressure per mossa** | `pressure = exp(-α ⋅ t)` con `t` = tempo residuo <br>`Δeval = perdita in centipawn` <br>`blame = Δeval ⋅ (1 - pressure)` | t→0 → pressure→1 (alta pressione → colpa ridotta) <br>t alto → pressure→0 (colpa piena) |
| **Time vs Quality curve** | correlazione tra tempo speso e accuracy / Δeval | insight su overthinking o sotto-pensiero |
| **Tempo medio per tipo di mossa** | media dei tempi su **blunder, mistake, inaccuracy, best move** | permette di vedere se i blunder arrivano sotto pressione |

---

## 3️⃣ Tilt / Momentum

**Obiettivo:** misurare la gestione emotiva e la stabilità decisionale.

| KPI | Formula / Metodo | Note |
|-----|-----------------|------|
| **Tilt score** | `tilt = w1*time_pressure + w2*error_rate + w3*streak` | definire w1, w2, w3 in base all’importanza dei fattori |
| **Streak positivi/negativi** | numero massimo di mosse consecutive Best/Splendid o blunder | utile per capire se il giocatore “entra in tilt” o “in flow” |

---

## 4️⃣ Controllo del tempo e gestione della partita

**Obiettivo:** capire se il giocatore usa bene il tempo disponibile.

| KPI | Formula / Metodo | Note |
|-----|-----------------|------|
| **Tempo medio per fase di gioco** | media dei tempi per apertura / mediogioco / finale | evidenzia se rallenta troppo nel finale o spreca tempo in apertura |
| **Tempo residuo medio a fine partita** | media tempo rimasto | utile per capire gestione complessiva |
| **Tempo vs Δeval** | correlazione tra tempo speso e perdita di centipawn | aiuta a identificare se il giocatore gioca meglio pensando di più o se overthinking porta errori |

---

## 5️⃣ Complessità della posizione e rischio

**Obiettivo:** capire come reagisce il giocatore in posizioni complicate.

| KPI | Formula / Metodo | Note |
|-----|-----------------|------|
| **Δeval per complessità** | `Δeval / CPL` o `Δeval / average CP loss` | CPL = centipawn loss medio della posizione |
| **Errori su posizioni critiche** | % mosse errate dove CPL > soglia | identifica se il giocatore gestisce bene posizioni complesse |
| **Decisione rapida vs complessità** | correlazione tempo speso / Δeval / complessità | insight su prontezza decisionale sotto stress |

---

## 6️⃣ Altri KPI avanzati

| KPI | Formula / Metodo | Note |
|-----|-----------------|------|
| **Opening performance** | media accuracy + Δeval mosse apertura | evidenzia forza teorica |
| **Endgame efficiency** | media Δeval finale / tempo speso finale | capacità di convertire vantaggi o difendere svantaggi |
| **Blame score** | `blame = Δeval ⋅ (1 - pressure)` aggregato per partita | uniforme tra mosse fatte sotto pressione e mosse con tempo sufficiente |
| **Consistency score** | deviazione standard Δeval / accuracy | alta deviazione → inconsistenza, bassa → giocatore stabile |

---

### 💡 Suggerimenti pratici

- Aggrega i dati **per partita e per giocatore** per KPI longitudinali.
- Usa **pandas** o **polars** per calcolare correlazioni e aggregazioni.
- Mantieni **fase di gioco** e **tempo speso** per ogni mossa.
- I KPI **basati sul tempo** (pressure, weighted accuracy, blame) sono quelli più differenzianti rispetto a strumenti standard.