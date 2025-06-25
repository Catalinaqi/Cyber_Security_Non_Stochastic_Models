import sys
import getpass
import logging
from enum import Enum, auto

# CONFIGURAZIONE INIZIALE
# Step 1: Configura il logging per tracciare il flusso di esecuzione
logging.basicConfig(
    #level=logging.DEBUG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Classe: State (Enum)
# Obiettivo: Definire i possibili stati del DFA di autenticazione
class State(Enum):
    START = auto()            # Stato iniziale: in attesa dell'username
    USERNAME_ENTERED = auto() # Username inserito, in attesa della password
    PASSWORD_ENTERED = auto() # Password inserita, in attesa di validazione
    AUTH_SUCCESS = auto()     # Autenticazione riuscita
    AUTH_FAILURE = auto()     # Autenticazione fallita

# Classe: LoginDFA
# Obiettivo: Gestire il flusso di autenticazione usando un DFA sincronizzato
# Step 2: Inizializza il DFA con lo stato START e le credenziali
# Step 3: Ricezione dell'username e transizione di stato
# Step 4: Ricezione della password e transizione di stato
# Step 5: Validazione delle credenziali e transizione di stato
class LoginDFA:
    def __init__(self, credentials: dict):
        """
        Metodo: __init__
        Obiettivo: Inizializza il DFA con lo stato START e carica il dizionario delle credenziali
        """
        # Step 2: Inizializza attributi
        self.state = State.START
        self.username_buffer = ''
        self.password_buffer = ''
        self.credentials = credentials
        logging.info(f"[Step 2][__init__] DFA inizializzato nello stato {self.state}")

    def input_username(self, user: str):
        """
        Metodo: input_username
        Obiettivo: Ricevere l'username dell'utente e fare la transizione di stato START/FAILURE -> USERNAME_ENTERED
        """
        # Step 3: Ricezione input dell'username
        logging.info(f"[Step 3][input_username] Chiamato con user='{user}' in stato {self.state}")
        if self.state in {State.START, State.AUTH_FAILURE}:
            self.username_buffer = user
            self.state = State.USERNAME_ENTERED
            logging.info(f"[Step 3][input_username] Transizione a {self.state}; username_buffer='{self.username_buffer}'")
        else:
            logging.error(f"[Step 3][input_username] Input inatteso in stato {self.state}")
            raise ValueError(f"Input inatteso 'username' in stato {self.state}")

    def input_password(self, pwd: str):
        """
        Metodo: input_password
        Obiettivo: Ricevere la password e fare la transizione USERNAME_ENTERED -> PASSWORD_ENTERED
        """
        # Step 4: Ricezione input della password
        logging.info(f"[Step 4][input_password] Chiamato in stato {self.state}")
        if self.state == State.USERNAME_ENTERED:
            self.password_buffer = pwd
            self.state = State.PASSWORD_ENTERED
            logging.info(f"[Step 4][input_password] Transizione a {self.state}; password_buffer='***'")
        else:
            logging.error(f"[Step 4][input_password] Input inatteso in stato {self.state}")
            raise ValueError(f"Input inatteso 'password' in stato {self.state}")

    def validate(self):
        """
        Metodo: validate
        Obiettivo: Verificare le credenziali e fare la transizione PASSWORD_ENTERED -> AUTH_SUCCESS/AUTH_FAILURE
        """
        # Step 5: Validazione delle credenziali
        logging.info(f"[Step 5][validate] Chiamato in stato {self.state}")
        if self.state != State.PASSWORD_ENTERED:
            logging.error(f"[Step 5][validate] Validazione inattesa in stato {self.state}")
            raise ValueError(f"Validazione inattesa in stato {self.state}")
        expected = self.credentials.get(self.username_buffer)
        if expected and expected == self.password_buffer:
            self.state = State.AUTH_SUCCESS
            logging.info(f"[Step 5][validate] Autenticazione riuscita per utente '{self.username_buffer}'")
            return True
        else:
            self.state = State.AUTH_FAILURE
            logging.warning(f"[Step 5][validate] Autenticazione fallita per utente '{self.username_buffer}'")
            return False

if __name__ == '__main__':
    # Step 6: Configurazione delle credenziali di esempio
    users = {
        'alice': 'pa$$w0rd',
        'bob': '123456'
    }

    # Step 7: Creazione istanza del DFA
    dfa = LoginDFA(users)
    print("Benvenuto al sistema di autenticazione")

    # Step 8: Ciclo principale di login
    while True:
        # Step 8.1: Inserimento dell'username da parte dell'utente
        username = input("Utente: ")
        dfa.input_username(username)

        # Step 8.2: Inserimento della password da parte dell'utente
        if sys.stdin.isatty():
            # Modalità interattiva → uso getpass per non echo della pwd
            password = getpass.getpass("Password: ")
        else:
            # No TTY (es. “Run” IDE) → fallback a input()
            password = input("Password: ")

        dfa.input_password(password)

        # Step 8.3: Validazione e risultato
        if dfa.validate():
            # Step 9: Accesso consentito -> termina il ciclo
            print("Accesso consentito!")
            break
        else:
            # Step 10: Accesso negato -> ripeti il ciclo
            print("Credenziali invalide. Riprova.\n")