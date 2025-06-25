# Applicazione di Login Sincrona con DFA

Questo readme ha l'obiettivo di illustrare in dettaglio l’algoritmo di autenticazione basato su un Automa Finito Deterministico (DFA) sincrono. Ogni fase del processo (inserimento username, inserimento password, validazione) è tracciata e descritta per evidenziare la logica delle transizioni di stato e facilitare la comprensione dell’implementazione.

---

## Indice

1. [Analisi del Modello DFA Sincrono](#analisi-del-modello-dfa-sincrono)
2. [Progettazione del Sistema](#progettazione-del-sistema)
3. [Concetti Chiave del DFA Sincrono](#concetti-chiave-del-dfa-sincrono)
4. [Flusso di Autenticazione](#flusso-di-autenticazione)
5. [Uso e Casi d’Uso](#uso-e-casi-duso)

    * [Casistica 1: Accesso Riuscito](#casistica-1-accesso-riuscito)
    * [Casistica 2: Credenziali Non Valide](#casistica-2-credenziali-non-valide)
    * [Casistica 3: Riprova Dopo Fallimento](#casistica-3-riprova-dopo-fallimento)
6. [Prossimi Passi ed Estensioni](#prossimi-passi-ed-estensioni)

---

## Progettazione e Analisi del DFA Sincrono

**Definizione formale del DFA**:

$M = (Q, Σ, δ, q₀, F)$

* **Q (Stati)**:

    * `START`
    * `USERNAME_ENTERED`
    * `PASSWORD_ENTERED`
    * `CREDENTIALS_SUBMITTED`
    * `AUTHENTICATED` (stato di accettazione)
    * `REJECTED` (stato di accettazione)

* **Σ: Sigma (Alfabeto di Input)**:

    * `ENTER_USERNAME`
    * `ENTER_PASSWORD`
    * `SUBMIT`
    * `VALID_SUCCESS`
    * `VALID_FAIL`

* **δ: delta (Funzione di Transizione)**:

  | From State              | Input Symbol     | To State                |
    | ----------------------- | ---------------- | ----------------------- |
  | `START`                 | `ENTER_USERNAME` | `USERNAME_ENTERED`      |
  | `USERNAME_ENTERED`      | `ENTER_PASSWORD` | `PASSWORD_ENTERED`      |
  | `PASSWORD_ENTERED`      | `SUBMIT`         | `CREDENTIALS_SUBMITTED` |
  | `CREDENTIALS_SUBMITTED` | `VALID_SUCCESS`  | `AUTHENTICATED`         |
  | `CREDENTIALS_SUBMITTED` | `VALID_FAIL`     | `REJECTED`              |

* **q₀ (Stato Iniziale)**: `START`

* **F (Stati di Accettazione)**: `{AUTHENTICATED, REJECTED}`

---

## Progettazione del Sistema

* **Obiettivo**: Implementare un login deterministico e tracciabile.
* **Dipendenze**:

    * Python 3.8+
    * `getpass`, `logging`, `enum`.
* **Componenti**:

    * **Classe State**: definisce gli stati tramite `enum.Enum`.
    * **Classe LoginDFA**: gestisce transizioni e validazione.
    * **Script Principale**: interfaccia CLI interattiva.

---

## Concetti Chiave del DFA Sincrono

1. **Determinismo**: transizione univoca per ogni input.
2. **Sincronia**: nessuna coda o callback, input elaborato immediatamente.
3. **Tracciabilità**: logging passo a passo.

---

## Flusso di Autenticazione

| Stato Attuale     | Input                 | Stato Successivo  |
| ----------------- | --------------------- | ----------------- |
| START             | input\_username(u)    | USERNAME\_ENTERED |
| USERNAME\_ENTERED | input\_password(p)    | PASSWORD\_ENTERED |
| PASSWORD\_ENTERED | validate (valido)     | AUTH\_SUCCESS     |
| PASSWORD\_ENTERED | validate (non valido) | AUTH\_FAILURE     |
| AUTH\_FAILURE     | input\_username(u)    | USERNAME\_ENTERED |

---

## Uso e Casi d’Uso

### Casistica 1: Accesso Riuscito

* **Descrizione**: Username e password corrette.
* **Output**:

  ```
  2025-06-25 10:00:00 - INFO - [Step 5][validate] Autenticazione riuscita per utente 'alice'
  Accesso consentito!
  ```

### Casistica 2: Credenziali Non Valide

* **Descrizione**: Password errata.
* **Output**:

  ```
  2025-06-25 10:05:00 - WARNING - [Step 5][validate] Autenticazione fallita per utente 'bob'
  Credenziali invalide. Riprova.
  ```

### Casistica 3: Riprova Dopo Fallimento

* **Descrizione**: Re-inserimento dopo AUTH\_FAILURE.
* **Output**:

  ```
  2025-06-25 10:05:00 - INFO - [Step 3][input_username] Transizione a USERNAME_ENTERED; username_buffer='bob'
  ```

---

## Prossimi Passi ed Estensioni

* Persistenza su database.
* Blocco account dopo N tentativi.
* Autenticazione a due fattori (2FA).
* Migrazione ad `asyncio`.
