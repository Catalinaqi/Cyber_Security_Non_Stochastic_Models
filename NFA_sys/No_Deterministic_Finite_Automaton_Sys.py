import logging
from typing import Set, Dict, Tuple

# Configurazione del logger per visualizzare informazioni passo-passo
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class NFA:
    """
    Classe NFA:
    - Scopo: rappresentare un Automa Finitamente Non Deterministico sincrono.
    - Motivazione: incapsulare stati e transizioni per modellare logicamente
      il flusso di validazione del login.
    """

    # Metodo di inizializzazione della classe NFA
    def __init__(
            self,
            states: Set[str],
            alphabet: Set[str],
            transitions: Dict[Tuple[str, str], Set[str]],
            start_state: str,
            accept_states: Set[str]
    ):
        # Inizializzazione degli attributi interni
        logger.info("Chiamato NFA.__init__: inizializzo attributi interni")
        self.states = states                  # Insieme di tutti gli stati possibili
        self.alphabet = alphabet              # Insieme dei simboli di input validi
        self.transitions = transitions        # Funzione di transizione: (stato, simbolo) -> stati successivi
        self.start_state = start_state        # Stato iniziale dell'automa
        self.accept_states = accept_states    # Stati di accettazione
        self.current_states = {start_state}   # Stati attivi in un dato momento

    # Metodo di reset dell'automa della classe NFA
    def reset(self) -> None:
        """
        Ripristina l'automa allo stato iniziale.
        Da richiamare prima di elaborare una nuova sequenza di simboli.
        """
        logger.info("Chiamato NFA.reset: ritorno allo stato iniziale '%s'", self.start_state)
        self.current_states = {self.start_state}

    # Metodo per elaborare un singolo simbolo di input della classe NFA
    def step(self, symbol: str, step_num: int) -> None:
        """
        Elabora un singolo simbolo di input in modo sincrono.

        Parametri:
        - symbol: simbolo corrente da processare (es. 'u', 'p').
        - step_num: indice del passo per il log.

        Scopo:
        - Calcolare il nuovo insieme di stati attivi a partire dagli stati correnti
          usando la funzione di transizione.
        - Annotare nel log lo stato precedente, il simbolo e i nuovi stati.
        """
        logger.info(f"Chiamato NFA.step (step_num={step_num}, symbol='{symbol}')")
        next_states: Set[str] = set()

        # Applico la transizione su ciascuno stato corrente
        for state in self.current_states:
            key = (state, symbol)
            if key in self.transitions:
                next_states |= self.transitions[key]

        # Log degli stati prima e dopo la transizione
        logger.info(f"  Stati precedenti: {self.current_states}")
        logger.info(f"  Nuovi stati:      {next_states}")
        self.current_states = next_states

    # Metodo per verificare se l'automa si trova in uno stato di accettazione della classe NFA
    def accepts(self) -> bool:
        """
        Verifica se l'automa si trova in uno stato di accettazione.

        Scopo:
        - Determinare se la sequenza elaborata è accettata dall'NFA.
        - Registrare nel log gli stati finali e l'esito.
        """
        logger.info("Chiamato NFA.accepts: controllo stati di accettazione")
        accepted = any(state in self.accept_states for state in self.current_states)
        logger.info(f"Stati finali: {self.current_states}")
        logger.info(f"Accettazione: {'SÌ' if accepted else 'NO'}")
        return accepted


# Metodo per costruire l'NFA specifico per il processo di login
def build_login_nfa() -> NFA:
    """
    Costruisce l'NFA per modellare il processo di login.

    Stati:
    - q0: stato iniziale (prima di verificare l'username).
    - q1: username valido, in attesa della password.
    - q2: login riuscito (stato di accettazione).
    - qf: stato di errore permanente.

    Alfabeto:
    - 'u': username corretto.
    - 'x': username errato.
    - 'p': password corretta.
    - 'y': password errata.

    Transizioni:
    - da q0: 'u' → q1, 'x' → qf.
    - da q1: 'p' → q2, 'y' → qf.
    - da qf: con qualsiasi simbolo → qf (stato di errore assorbente).
    """
    logger.info("Chiamato build_login_nfa: definizione di stati, alfabeto e transizioni")
    states = {'q0', 'q1', 'q2', 'qf'}
    alphabet = {'u', 'x', 'p', 'y'}
    transitions: Dict[Tuple[str, str], Set[str]] = {
        ('q0', 'u'): {'q1'},
        ('q0', 'x'): {'qf'},
        ('q1', 'p'): {'q2'},
        ('q1', 'y'): {'qf'},
        # Stato di errore assorbe tutti i simboli
        ('qf', 'u'): {'qf'}, ('qf', 'x'): {'qf'},
        ('qf', 'p'): {'qf'}, ('qf', 'y'): {'qf'},
    }
    start_state = 'q0'
    accept_states = {'q2'}
    nfa = NFA(states, alphabet, transitions, start_state, accept_states)
    logger.info("NFA di login costruito correttamente")
    return nfa


# Metodo per gestire il processo di login usando l'NFA
def login_process(nfa: NFA, credentials: Dict[str, str]) -> None:
    """
    Processo interattivo di login usando l'NFA.

    Step:
    1. Chiedere username e password all'utente.
    2. Tradurre la validità di ciascun dato in simboli NFA ('u'/'x', 'p'/'y').
    3. Ripristinare l'automa.
    4. Iterare sui simboli e chiamare nfa.step() (log interno).
    5. Chiamare nfa.accepts() per verificare successo o fallimento.
    """
    logger.info("Chiamato login_process: avvio del processo di login")
    # 1. Input dell'utente
    input_username = input("Inserisci username: ")
    input_password = input("Inserisci password: ")
    logger.info(f"  Input ricevuto: username='{input_username}', password='{'*'*len(input_password)}'")
    # 2. Mappatura in simboli dell'NFA
    symbols = []
    symbols.append('u' if input_username in credentials else 'x')
    symbols.append('p' if credentials.get(input_username) == input_password else 'y')
    logger.info(f"  Simboli generati per NFA: {symbols}")

    # 3. Reset dell'automa prima dell'elaborazione
    nfa.reset()
    # 4. Esecuzione passo-passo con log
    for idx, sym in enumerate(symbols, start=1):
        nfa.step(sym, idx)

    # 5. Verifica accettazione
    result = nfa.accepts()
    if result:
        print("Login riuscito. Benvenuto!")
    else:
        print("Login fallito. Riprova.")
    logger.info("login_process completato con esito: %s", 'SUCCESSO' if result else 'FALLIMENTO')



# Metodo principale per avviare il processo di login
if __name__ == '__main__':
    logger.info("---- Avvio script di login ----")
    # Credenziali di esempio per la demo
    demo_credentials = {
        'alice': 'password123',
        'bob':   'qwerty',
    }

    # Costruzione dell'NFA per il login
    nfa = build_login_nfa()
    # Avvio del processo di login
    login_process(nfa, demo_credentials)

    # Log di fine esecuzione
    logger.info("---- Processo di login completato ----")
