# Applicazione di Login Asincrona con NFA

Questo README descrive in dettaglio l’applicazione di autenticazione basata su un Automa a Stati Finiti Non Deterministico (NFA) **asincrono**.
Ogni fase del processo (costruzione dell’automa, inserimento username, inserimento password, validazione) è tracciata passo per passo tramite il logger, evidenziando la logica delle transizioni di stato e facilitando la comprensione dell’implementazione.

---

## Indice

1. [Analisi del Modello NFA Asincrono](#analisi-del-modello-nfa-asincrono)
2. [Progettazione del Sistema](#progettazione-del-sistema)
3. [Concetti Chiave del NFA Asincrono](#concetti-chiave-del-nfa-asincrono)
4. [Flusso di Autenticazione](#flusso-di-autenticazione)
5. [Uso e Casi d’Uso](#uso-e-casi-duso)

    * Caso 1: Accesso Riuscito
    * Caso 2: Credenziali Non Valide
    * Caso 3: Errore di Sistema Permanente
6. [Prossimi Passi ed Estensioni](#prossimi-passi-ed-estensioni)

---

## Analisi del Modello NFA Asincrono

Definizione formale dell’NFA:

```
M = (Q, Σ, δ, q₀, F)
```

* **Q (Stati)**

    * `q0` : stato iniziale (nessun input ancora ricevuto)
    * `q1` : username validato, in attesa password
    * `q2` : autenticazione riuscita (stato di accettazione)
    * `qf` : stato di fallimento (assorbente)

* **Σ (Alfabeto)**

    * `u` : username corretto (“admin”)
    * `x` : username non riconosciuto
    * `p` : password corretta (“secret”)
    * `y` : password errata

* **δ (Funzione di Transizione)**

  | From State | Input Symbol | To State |
    | :--------: | :----------: | :------: |
  |     q0     |       u      |    q1    |
  |     q0     |       x      |    qf    |
  |     q1     |       p      |    q2    |
  |     q1     |       y      |    qf    |
  |     qf     |  *qualsiasi* |    qf    |

* **q₀ (Stato Iniziale)**: `q0`

* **F (Stati di Accettazione)**: `{ q2 }`

> *Nota*: l’esecuzione è **asincrona** per simulare il branching nondeterministico, ma la logica di transizione rimane identica.

---

## Progettazione del Sistema

* **Obiettivo**
  Fornire un login asincrono, tracciabile passo per passo tramite un NFA.

* **Dipendenze**

    * Python 3.8+
    * librerie standard: `asyncio`, `logging`, `dataclasses`, `typing`

* **Componenti**

    1. **Classe `State`**

        * Modella uno stato dell’automa, con transizioni normali ed ε.
        * Implementa `__hash__` per poter usare insiemi di stati.
    2. **Classe `NFA`**

        * Espone i metodi `epsilon_closure(states)` e `async run(input_string)`.
        * Log step-by-step delle transizioni e chiusure ε.
    3. **Funzione `build_nfa_for_string(target: str) -> NFA`**

        * Costruisce un NFA “lineare” che accetta esattamente la stringa `target`.
    4. **Funzione `main()`**

        * Gestisce l’interazione CLI, legge input e invoca `await nfa.run(...)`.
    5. **Script Principale**

        * `asyncio.run(main())` avvia l’intera procedura.

---

## Concetti Chiave del NFA Asincrono

* **ε-closure**
  Espande un insieme di stati includendo tutte le transizioni ε (anche se non utilizzate in questo esempio).
* **Branching nondeterministico**
  Simulato con `await asyncio.sleep(0)` ad ogni passo del run.
* **Logger dettagliato**
  Ogni metodo e passaggio logga l’obiettivo e lo stato corrente, per facilitare il debug.

---

## Flusso di Autenticazione

1. **Avvio**

    * `[main]` inizializza la procedura
    * Invoca `build_nfa_for_string("admin")` e `build_nfa_for_string("secret")`
2. **Input**

    * Lettura di `Username` e `Password` via `input()`
3. **Verifica Username**

    * `await nfa_user.run(username)`
    * Log di ogni step (stati iniziali, transizioni, chiusure ε, esito)
4. **Verifica Password**

    * Se lo username è valido, `await nfa_pwd.run(password)`
5. **Esito**

    * Stampa `Login eseguito con successo!` o messaggio di errore

---

## Uso e Casi d’Uso

### Caso 1: Accesso Riuscito

**Input**

```
Username: admin  
Password: secret  
```

**Output atteso in console**

```
[main] Avvio procedura login asincrona
[main] Invocazione -> build_nfa_for_string('admin')
… transizioni e log dettagliati …
[main] Invocazione -> build_nfa_for_string('secret')
Username: admin
Password: ***
[main] Invocazione -> NFA.run su USERNAME
Step 0 — Stati iniziali: ['q0']
Step 1 — ingresso 'a' … → ['q1']
… fino a q2 …
[NFA.run] Esito finale: ACCETTATO
[main] Invocazione -> NFA.run su PASSWORD
… log simili per 'secret' …
[NFA.run] Esito finale: ACCETTATO
Login eseguito con successo!
```

### Caso 2: Credenziali Non Valide

* **Username errato**

  ```
  Username: guest  
  Password: secret  
  ```

  **Output**

  ```
  Login fallito: username non valido.
  ```

* **Password errata**

  ```
  Username: admin  
  Password: 1234  
  ```

  **Output**

  ```
  Login fallito: password errata.
  ```

### Caso 3: Errore di Sistema Permanente

* **Situazione**
  Eccezione imprevista durante la costruzione o l’esecuzione dell’NFA.
* **Output**

  ```
  Errore interno, riprovare più tardi.
  ```

---

## Prossimi Passi ed Estensioni

* Abilitare transizioni ε per pattern più flessibili
* Connessione a un database per gestire utenti dinamici
* Interfaccia Web con FastAPI o aiohttp
* Logging avanzato (file, livelli differenziati, formati JSON)

---

Con questa struttura **asincrona** e il logging dettagliato, il funzionamento dell’algoritmo NFA risulta completamente tracciabile e modulare.
