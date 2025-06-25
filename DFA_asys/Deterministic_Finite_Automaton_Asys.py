import asyncio
import getpass
import hashlib
import logging
import sys


# Configurazione base del logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Classe che implementa un Automa a Stati Finiti (DFA) asincrono per la gestione del login
class AsyncDFALogin:
    """
    Automa a stati finiti asincrono che gestisce il flusso di login:
      1) lettura username
      2) validazione username
      3) lettura password (con max tentativi)
      4) validazione password
    Registra in log ogni step numerato.
    """

    # Metodo di inizializzazione
    def __init__(self, users_db: dict):
        """
        Inizializza stati, transizioni, contatore di step e database utenti.
        :param users_db: dizionario username→password_hash
        """
        # Stati
        self.initial_state = "start"
        self.accept_state = "authenticated"
        self.error_state = "error"

        # Transizioni DFA: (stato_corrente, evento) → stato_successivo
        self.transitions = {
            ("start",       "input_user"):  "check_user",
            ("check_user",  "valid_user"):  "check_pass",
            ("check_user",  "invalid_user"):"error",
            ("check_pass",  "input_pass"):  "check_pass",
            ("check_pass",  "valid_pass"):  "authenticated",
            ("check_pass",  "invalid_pass"):"error",
        }

        self.users_db = users_db
        self.step = 0
        self.logger = logging.getLogger(self.__class__.__name__)

    # Metodo per leggere l'username e la password in modo asincrono
    async def read_username(self) -> str:
        """
        Step: input_user
        Lanza input() en un thread pool para no bloquear el event‐loop.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, "Username: ")

    # Metodo per leggere la password in modo asincrono
    async def read_password(self) -> str:
        """
        Step: input_pass
        - Se siamo in TTY, uso getpass.getpass (niente eco).
        - Altrimenti (console “Run” senza TTY), ritraccio l’input con input().
        """
        loop = asyncio.get_event_loop()

        if sys.stdin.isatty() and sys.stdout.isatty():
            # vero terminale → nascondi l’eco
            return await loop.run_in_executor(
                None,
                getpass.getpass,
                "Password: "
            )
        else:
            # fallback a input() per forzare la lettura
            print("Password: ", end="", flush=True)
            return await loop.run_in_executor(None, input)

    # Metodo per calcolare l'hash della password
    def hash_password(self, password: str) -> str:
        """Calcola e restituisce l’hash SHA-256 della password in chiaro."""
        return hashlib.sha256(password.encode()).hexdigest()

    # Metodo per validare l'username
    async def validate_user(self, username: str) -> bool:
        """Step: valid_user/invalid_user — controlla se l’username esiste."""
        await asyncio.sleep(0)
        return username in self.users_db

    # Metodo per validare la password
    async def validate_password(self, username: str, password: str) -> bool:
        """Step: valid_pass/invalid_pass — controlla se la password è corretta."""
        await asyncio.sleep(0)
        return self.users_db.get(username) == self.hash_password(password)

    # Metodo principale che esegue l'automa
    async def run(self, max_pass_attempts: int = 3) -> bool:
        """
        Esegue l’automa:
         - legge e valida username
         - in caso di utente valido, richiede la password (fino a max_pass_attempts tentativi)
         - effettua il log di ogni transizione con numero di step
        :return: True se autenticato, False altrimenti
        """
        state = self.initial_state
        self.logger.info("DFA login start")

        # --- STEP 1: input_user ---
        self.step += 1
        self.logger.info(f"Step {self.step}: evento='input_user', stato_precedente='{state}'")
        state = self.transitions.get((state, "input_user"), self.error_state)

        # Lettura username
        username = await self.read_username()

        # --- STEP 2: valid_user / invalid_user ---
        is_valid_user = await self.validate_user(username)
        evento = "valid_user" if is_valid_user else "invalid_user"
        self.step += 1
        self.logger.info(f"Step {self.step}: evento='{evento}', stato_precedente='check_user'")
        state = self.transitions.get(("check_user", evento), self.error_state)

        if state == self.error_state:
            print("Utente non riconosciuto.")
            return False

        # --- STEP 3: ciclo password fino a max_pass_attempts ---
        # Prima transizione per 'input_pass'
        self.step += 1
        self.logger.info(f"Step {self.step}: evento='input_pass', stato_precedente='check_pass'")
        state = self.transitions.get((state, "input_pass"), self.error_state)

        for attempt in range(1, max_pass_attempts + 1):
            # Lettura password
            password = await self.read_password()

            # Validazione password
            is_valid_pass = await self.validate_password(username, password)
            evento = "valid_pass" if is_valid_pass else "invalid_pass"
            self.step += 1
            self.logger.info(
                f"Step {self.step}: tentativo_password={attempt}, evento='{evento}', stato_precedente='check_pass'"
            )
            state = self.transitions.get(("check_pass", evento), self.error_state)

            if state == self.accept_state:
                print(f"Accesso effettuato con successo. Benvenuto, {username}!")
                return True

            # Se password sbagliata e restano tentativi, riprova
            if attempt < max_pass_attempts:
                print("Password errata, riprova.")
                # rimettiamo lo stato su 'check_pass' e facciamo un nuovo input_pass
                self.step += 1
                self.logger.info(f"Step {self.step}: evento='input_pass' per retry, stato_precedente='error'")
                state = self.transitions.get((self.error_state, "input_pass"), "check_pass")

        # Se esauriti i tentativi
        print("Numero tentativi esaurito. Accesso negato.")
        return False

# Esecuzione del DFA asincrono
if __name__ == "__main__":
    # Esempio di database iniziale
    users_db = {
        "alice": hashlib.sha256("wonderland".encode()).hexdigest(),
        "bob":   hashlib.sha256("builder".encode()).hexdigest(),
    }

    # Esecuzione asincrona
    dfa = AsyncDFALogin(users_db)
    # Lanza la coroutine y cierra correctamente el event‐loop
    asyncio.run(dfa.run())
