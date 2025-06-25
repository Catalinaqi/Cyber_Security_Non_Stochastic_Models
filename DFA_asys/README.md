# Applicazione di Login Asincrona con DFA

Questo README ha l'obiettivo di descrivere in dettaglio l'implementazione di un sistema di autenticazione basato su un Automa Finitio Deterministico (DFA) **asincrono**, sfruttando `asyncio` per gestire in modo non bloccante le operazioni di input/output. Ogni fase del processo (inserimento username, inserimento password, validazione) è tracciata tramite logging e commentata per facilitarne la comprensione.

---

## Indice

1. [Modello DFA Asincrono](#modello-dfa-asincrono)
2. [Progettazione del Sistema](#progettazione-del-sistema)
3. [Componenti Principali](#componenti-principali)
4. [Flusso di Esecuzione](#flusso-di-esecuzione)
5. [Esempi di Esecuzione](#esempi-di-esecuzione)
6. [Estensioni Future](#estensioni-future)

---

## 1. Modello DFA Asincrono

Definizione formale dell'automa $M = (Q, Σ, δ, q₀, F)$:

* **Q (Stati):**

  * `START`
  * `CHECK_USER`
  * `CHECK_PASS`
  * `AUTHENTICATED` (stato di accettazione)
  * `ERROR`

* **Σ (Alfabeto di Input):**

  * `input_user`
  * `valid_user` / `invalid_user`
  * `input_pass`
  * `valid_pass` / `invalid_pass`

* **δ (Funzione di Transizione):**

  | From State   | Input Symbol   | To State        |
    | ------------ | -------------- | --------------- |
  | `START`      | `input_user`   | `CHECK_USER`    |
  | `CHECK_USER` | `valid_user`   | `CHECK_PASS`    |
  | `CHECK_USER` | `invalid_user` | `ERROR`         |
  | `CHECK_PASS` | `input_pass`   | `CHECK_PASS`    |
  | `CHECK_PASS` | `valid_pass`   | `AUTHENTICATED` |
  | `CHECK_PASS` | `invalid_pass` | `ERROR`         |

* **q₀ (Stato iniziale):** `START`

* **F (Stati di Accettazione):** {`AUTHENTICATED`}

---

## 2. Progettazione del Sistema

* **Obiettivo:** Implementare un login asincrono, tracciabile con logging dettagliato per ogni step.
* **Dipendenze:**

  * Python 3.8+
  * Moduli: `asyncio`, `getpass`, `logging`, `hashlib`

---

## 3. Componenti Principali

* **Classe `AsyncDFALogin`**

  * Gestisce stati, transizioni, contatore di step e logger.
  * Documenta ogni metodo con docstring che spiega lo scopo.

* **Funzioni di Input**

  * `read_username()`: legge l'username in executor non bloccante.
  * `read_password()`: legge la password senza eco (o con fallback a `input()`).

* **Metodi di Validazione**

  * `validate_user()`: verifica presenza dell'username nel database.
  * `validate_password()`: confronta hash della password.

---

## 4. Flusso di Esecuzione

1. **Avvio**: `asyncio.run(dfa.run())` lancia il DFA dal `START`.
2. **Input Username** (`input_user`) → transizione a `CHECK_USER`.
3. **Validazione Username** (`valid_user` o `invalid_user`):

  * Se valido → `CHECK_PASS`, altrimenti terminazione con `ERROR`.
4. **Input Password** (`input_pass`) e validazione (`valid_pass`/`invalid_pass`):

  * Ciclo di retry (default 3 tentativi) su `CHECK_PASS`.
5. **Stato Finale**:

  * Se `AUTHENTICATED`: accesso consentito.
  * Se `ERROR`: accesso negato.

Durante ogni passaggio, un contatore `step` e il logger registrano timestamp, stato precedente ed evento.

---

## 5. Esempi di Esecuzione

```bash
$ python Deterministic_Finite_Automaton_Asys.py
[2025-06-25 12:00:00] DFA login start
[2025-06-25 12:00:00] Step 1: evento='input_user', stato_precedente='START'
Username: alice
[2025-06-25 12:00:05] Step 2: evento='valid_user', stato_precedente='CHECK_USER'
[2025-06-25 12:00:05] Step 3: evento='input_pass', stato_precedente='CHECK_PASS'
Password:
[2025-06-25 12:00:10] Step 4: evento='valid_pass', stato_precedente='CHECK_PASS'
Accesso effettuato con successo. Benvenuto, alice!
```

---

## 6. Estensioni Future

* Supporto multi-tenant e database esterno
* Audit delle transizioni su file CSV o DB
* Interfaccia web asincrona con FastAPI
* Configurazione dinamica degli stati e transizioni via file YAML
