import asyncio
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Set

# ─── Configurazione del logger ─────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@dataclass
class State:
    """
    Classe State: rappresenta uno stato dell'NFA.
    Obiettivo: mantenere nome, transizioni normali ed epsilon.
    """
    name: str
    transitions: Dict[str, List['State']] = field(default_factory=dict)
    epsilon_transitions: List['State'] = field(default_factory=list)
    is_accept: bool = False

    def __hash__(self):
        # Permette di inserire State in set e dict
        return id(self)

    def add_transition(self, symbol: str, state: 'State'):
        """Metodo State.add_transition: aggiunge una transizione etichettata."""
        logging.info(f"[State.add_transition] Obiettivo: collegare stato '{self.name}' → '{state.name}' via '{symbol}'")
        self.transitions.setdefault(symbol, []).append(state)

    def add_epsilon(self, state: 'State'):
        """Metodo State.add_epsilon: aggiunge una transizione ε."""
        logging.info(f"[State.add_epsilon] Obiettivo: collegare stato '{self.name}' → '{state.name}' via ε")
        self.epsilon_transitions.append(state)

class NFA:
    """
    Classe NFA: automa non deterministico asincrono.
    Obiettivo: simulare un NFA su una stringa di input.
    """
    def __init__(self, start_state: State, accept_states: Set[State]):
        logging.info(f"[NFA.__init__] Obiettivo: inizializzare NFA con start={start_state.name}, accept={[s.name for s in accept_states]}")
        self.start_state = start_state
        self.accept_states = accept_states

    def epsilon_closure(self, states: Set[State]) -> Set[State]:
        """
        Metodo NFA.epsilon_closure:
        Obiettivo: espandere lo stato corrente includendo transizioni ε ricorsive.
        """
        logging.info(f"[NFA.epsilon_closure] Obiettivo: calcolare chiusura ε di {[s.name for s in states]}")
        stack = list(states)
        closure = set(states)
        while stack:
            st = stack.pop()
            for nxt in st.epsilon_transitions:
                if nxt not in closure:
                    logging.info(f"  ε-chiusura: aggiungo stato '{nxt.name}' da '{st.name}'")
                    closure.add(nxt)
                    stack.append(nxt)
        logging.info(f"[NFA.epsilon_closure] Risultato chiusura ε: {[s.name for s in closure]}")
        return closure

    async def run(self, input_string: str) -> bool:
        """
        Metodo NFA.run:
        Obiettivo: eseguire l'NFA su input_string in modo asincrono, restituendo True se accettato.
        """
        logging.info(f"[NFA.run] Obiettivo: avvio esecuzione NFA su '{input_string}'")
        # Step 0: epsilon-chiusura iniziale
        current_states = self.epsilon_closure({self.start_state})
        logging.info(f"Step 0 — Stati iniziali: {[s.name for s in current_states]}")

        # Iterazione sui simboli
        for idx, symbol in enumerate(input_string, start=1):
            logging.info(f"[NFA.run] Step {idx} — ingresso simbolo '{symbol}'")
            next_states: Set[State] = set()
            for st in current_states:
                targets = st.transitions.get(symbol, [])
                for tgt in targets:
                    logging.info(f"  da {st.name} → {tgt.name} tramite '{symbol}'")
                    next_states.add(tgt)
            # epsilon-chiusura del passo
            current_states = self.epsilon_closure(next_states)
            logging.info(f"Step {idx} — stati dopo ε-chiusura: {[s.name for s in current_states]}")
            await asyncio.sleep(0)  # yield per simulare branching

        # Verifica accettazione
        accepted = any(st in self.accept_states for st in current_states)
        logging.info(f"[NFA.run] Esito finale: {'ACCETTATO' if accepted else 'RIFIUTATO'}")
        return accepted

def build_nfa_for_string(target: str) -> NFA:
    """
    Funzione build_nfa_for_string:
    Obiettivo: costruire un NFA che accetta esattamente la stringa target.
    """
    logging.info(f"[build_nfa_for_string] Obiettivo: creare NFA per '{target}'")
    states = [State(f"q{i}") for i in range(len(target) + 1)]
    states[-1].is_accept = True
    for i, ch in enumerate(target):
        states[i].add_transition(ch, states[i+1])
    return NFA(start_state=states[0], accept_states={states[-1]})

async def main():
    logging.info("[main] Obiettivo: avvio procedura login asincrona")

    # 1) Creazione NFA per l’username
    logging.info("[main] Invocazione -> build_nfa_for_string(target='admin')")
    nfa_user = build_nfa_for_string("admin")
    logging.info(f"[main] Completato -> NFA USER: start={nfa_user.start_state.name}, accept={[s.name for s in nfa_user.accept_states]}")

    # 2) Creazione NFA per la password
    logging.info("[main] Invocazione -> build_nfa_for_string(target='secret')")
    nfa_pwd = build_nfa_for_string("secret")
    logging.info(f"[main] Completato -> NFA PWD: start={nfa_pwd.start_state.name}, accept={[s.name for s in nfa_pwd.accept_states]}")

    # Input utente
    logging.info("[main] Chiamata -> input('Username: ')")
    username = input("Username: ")
    logging.info(f"[main] Inserito USERNAME: '{username}'")
    logging.info("[main] Chiamata -> input('Password: ')")
    password = input("Password: ")
    logging.info("[main] Inserita PASSWORD: '***'")

    # 3) Verifica username
    logging.info("[main] Invocazione -> NFA.run su USERNAME")
    ok_user = await nfa_user.run(username)
    logging.info(f"[main] NFA.run USERNAME restituito: {ok_user}")
    if not ok_user:
        print("Login fallito: username non valido.")
        return

    # 4) Verifica password
    logging.info("[main] Invocazione -> NFA.run su PASSWORD")
    ok_pwd = await nfa_pwd.run(password)
    logging.info(f"[main] NFA.run PASSWORD restituito: {ok_pwd}")
    if not ok_pwd:
        print("Login fallito: password errata.")
    else:
        print("Login eseguito con successo!")


if __name__ == "__main__":
    asyncio.run(main())
