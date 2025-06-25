# Applicazione di Login Sincro con NFA

Questo README descrive in dettaglio l'applicazione di autenticazione basata su un Autom a Stati Finiti Non Deterministico (NFA) sincrono. Ogni fase del processo (inserimento username, inserimento password, validazione) è tracciata passo per passo, evidenziando la logica delle transizioni di stato e facilitando la comprensione dell’implementazione.

---

## Indice

1. [Analisi del Modello NFA Sincrono](#analisi-del-modello-nfa-sincrono)
2. [Progettazione del Sistema](#progettazione-del-sistema)
3. [Concetti Chiave del NFA Sincrono](#concetti-chiave-del-nfa-sincrono)
4. [Flusso di Autenticazione](#flusso-di-autenticazione)
5. [Uso e Casi d’Uso](#uso-e-casi-duso)

  * Caso 1: Accesso Riuscito
  * Caso 2: Credenziali Non Valide
  * Caso 3: Errore Permanente
6. [Prossimi Passi ed Estensioni](#prossimi-passi-ed-estensioni)

---

## Analisi del Modello NFA Sincrono

Definizione formale dell'NFA:

> **M** = (Q, Σ, δ, q₀, F)

* **Q** (Stati)

  * `q0` : stato iniziale (nessun input ancora ricevuto)
  * `q1` : username validato, in attesa password
  * `q2` : autenticazione riuscita (stato di accettazione)
  * `qf` : stato di fallimento assorbente

* **Σ** (Alfabeto)

  * `u` : username corretto
  * `x` : username non riconosciuto
  * `p` : password corretta
  * `y` : password errata

* **δ** (Funzione di Transizione)

  | From State | Input Symbol | To State          |
    | ---------- | ------------ | ----------------- |
  | `q0`       | `u`          | `q1`              |
  | `q0`       | `x`          | `qf`              |
  | `q1`       | `p`          | `q2`              |
  | `q1`       | `y`          | `qf`              |
  | `qf`       | *qualsiasi*  | `qf` (assorbente) |

* **q₀** (Stato Iniziale): `q0`

* **F** (Stati di Accettazione): `{ q2 }`

---

## Progettazione del Sistema

* **Obiettivo**: fornire un login sincrono, tracciabile passo per passo tramite un NFA.

* **Dipendenze**:

  * Python 3.8+
  * librerie standard: `logging`, `typing` (per i tipi)

* **Componenti**:

  1. **Classe `NFA`**: modellizza stati, alfabeto, transizioni e log step-by-step.
  2. **Funzione `build_login_nfa()`**: costruisce l’automa del login con stati e transizioni predefinite.
  3. **Funzione `login_process()`**: gestisce l’interazione CLI, traduce input in simboli e invoca il NFA.
  4. **Script Principale**: inizializza credenziali demo, crea l’NFA e avvia il processo.

---

## Concetti Chiave del NFA Sincrono

1. **Non Determinismo**: l’automa può occupare simultaneamente più stati, ma nel nostro modello rimane determinato per semplicità.
2. **Sincronia**: ogni simbolo è elaborato immediatamente e in blocco senza callback o code.
3. **Tracciabilità**: `logging` registra ogni chiamata a `step()`, `reset()` e `accepts()`, mostrando stati precedenti e successivi.
4. **Assorbimento**: lo stato di fallimento `qf` cattura ogni simbolo e previene ulteriori transizioni verso stati validi.

---

## Flusso di Autenticazione

1. **Avvio**: lo script stampa nel log l’avvio (`main`).
2. **Costruzione NFA**: `build_login_nfa()` definisce e stampa nel log la creazione dell’automa.
3. **Input Utente**: `login_process()` legge username e password da CLI, loggando l’input (password camuffata).
4. **Mappatura Simboli**: genera la lista `['u'/'x', 'p'/'y']` e la registra nel log.
5. **Reset Automa**: `nfa.reset()` riporta al simbolo iniziale `q0` e lo registra.
6. **Step a Step**: per ogni simbolo:

  * `nfa.step(symbol, idx)` logga il passo, gli stati prima e dopo.
7. **Verifica**: `nfa.accepts()` controlla se `q2 ∈ current_states`, loggando esito e stati finali.
8. **Output**: stampa a video "Login riuscito" o "Login fallito".
9. **Chiusura**: log finale del completamento del processo.

---

## Uso e Casi d’Uso

In questa sezione sono riportati esempi di esecuzione del programma in console, con input simulato e output atteso (log passo‑step e risultato finale).

### Caso 1: Accesso Riuscito

**Input:**

```text
Username: alice
Password: password123
```

**Output atteso in console:**

```text
[INFO] ---- Avvio script di login ----
[INFO] Chiamato build_login_nfa: definizione di stati, alfabeto e transizioni
[INFO] NFA di login costruito correttamente
[INFO] Chiamato login_process: avvio del processo di login
[INFO]   Input ricevuto: username='alice', password='*************'
[INFO]   Simboli generati per NFA: ['u', 'p']
[INFO] Chiamato NFA.reset: ritorno allo stato iniziale 'q0'
[INFO] Chiamato NFA.step (step_num=1, symbol='u')
  Stati precedenti: {'q0'}
  Nuovi stati:      {'q1'}
[INFO] Chiamato NFA.step (step_num=2, symbol='p')
  Stati precedenti: {'q1'}
  Nuovi stati:      {'q2'}
[INFO] Chiamato NFA.accepts: controllo stati di accettazione
  Stati finali: {'q2'}
  Accettazione: SÌ
Login riuscito. Benvenuto!
[INFO] login_process completato con esito: SUCCESSO
[INFO] ---- Processo di login completato ----
```

### Caso 2: Username Errato

**Input:**

```text
Username: unknown
Password: anypass
```

**Output atteso in console:**

```text
[INFO] ---- Avvio script di login ----
[INFO] Chiamato build_login_nfa: definizione di stati, alfabeto e transizioni
[INFO] NFA di login costruito correttamente
[INFO] Chiamato login_process: avvio del processo di login
[INFO]   Input ricevuto: username='unknown', password='*******'
[INFO]   Simboli generati per NFA: ['x', 'y']
[INFO] Chiamato NFA.reset: ritorno allo stato iniziale 'q0'
[INFO] Chiamato NFA.step (step_num=1, symbol='x')
  Stati precedenti: {'q0'}
  Nuovi stati:      {'qf'}
[INFO] Chiamato NFA.step (step_num=2, symbol='y')
  Stati precedenti: {'qf'}
  Nuovi stati:      {'qf'}
[INFO] Chiamato NFA.accepts: controllo stati di accettazione
  Stati finali: {'qf'}
  Accettazione: NO
Login fallito. Riprova.
[INFO] login_process completato con esito: FALLIMENTO
[INFO] ---- Processo di login completato ----
```

### Caso 3: Password Errata

**Input:**

```text
Username: bob
Password: wrongpass
```

**Output atteso in console:**

````text
[INFO] ---- Avvio script di login ----
[INFO] Chiamato build_login_nfa: definizione di stati, alfabeto e transizioni
[INFO] NFA di login costruito correttamente
[INFO] Chiamato login_process: avvio del processo di login
[INFO]   Input ricevuto: username='bob', password='*********'
[INFO]   Simboli generati per NFA: ['u', 'y']
[INFO] Chiamato NFA.reset: ritorno allo stato iniziale 'q0'
[INFO] Chiamato NFA.step (step_num=1, symbol='u')
  Stati precedenti: {'q0'}
  Nuovi stati:      {'q1'}
[INFO] Chiamato NFA.step (step_num=2, symbol='y')
  Stati precedenti: {'q1'}
  Nuovi stati:      {'qf'}
[INFO] Chiamato NFA.accepts: controllo stati di accettazione
  Stati finali: {'qf'}
  Accettazione: NO
Login fallito. Riprova.
[INFO] login_process completato con esito: FALLIMENTO
```---

## Prossimi Passi ed Estensioni

- Supporto a più tentativi con contatore e lock-out temporaneo.
- Lettura credenziali da database o file esterno anziché dizionario hard‑coded.
- Interfaccia grafica o API REST per integrazione in server.
- Aggiunta di epsilon-transizioni per modellare flussi più complessi.
- Estensione a NFA multiplo con possibili transizioni parallele e branching.

````
