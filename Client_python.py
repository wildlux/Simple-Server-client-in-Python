# client.py
import socket
import time
import config

HOST = config.HOST_IP
PORT = config.PORTA_SERVER
TIMEOUT = config.TIMEOUT_CONNESSIONE

def esegui_azione(azione):
    """Funzione che simula l'esecuzione del servizio richiesto dal Server."""
    if azione == "OK_MUSICA":
        print("\n*** Servizio Avviato ***")
        print("🎶 Avvio della musica...")
        time.sleep(1)
        print("🎶 Musica terminata.")
        print("***********************\n")
    elif azione == "OK_MESSAGGIO":
        print("\n*** Servizio Avviato ***")
        print("✍️ Scrittura sul prompt: 'Il servizio è stato avviato correttamente!'")
        print("***********************\n")
    else:
        print(f"Risposta del server non gestita: {azione}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        # Imposta il timeout prima di tentare la connessione
        s.settimeout(TIMEOUT)

        # Tenta la connessione
        s.connect((HOST, PORT))
        print(f"Connesso al server su {HOST}:{PORT}")

        # Se la connessione ha successo, rimuovi il timeout
        # in modo che il client aspetti l'input dell'utente senza scadere.
        s.settimeout(None)

        while True:
            comando_utente = input("Comandi disponibili (MUSICA, MESSAGGIO, CIAO): ").upper()
            if not comando_utente:
                continue

            # Reimposta un piccolo timeout per l'invio/ricezione
            # per evitare blocchi infiniti.
            s.settimeout(TIMEOUT)

            # Invia il comando
            s.sendall(comando_utente.encode('utf-8'))

            if comando_utente == "CIAO":
                print("Disconnessione richiesta.")
                break

            # Ricevi la risposta
            risposta = s.recv(1024).decode('utf-8').strip()
            print(f"Ricevuto dal Server: {risposta}")

            # Esegui il servizio
            if risposta.startswith("OK_"):
                esegui_azione(risposta)

            s.settimeout(None) # Rimuovi il timeout dopo l'interazione per il prossimo input

    except socket.timeout:
        print(f"Errore: Timeout (scaduto il tempo massimo di {TIMEOUT}s) durante la connessione o la comunicazione.")
    except ConnectionRefusedError:
        print(f"Errore: Impossibile connettersi al server su {HOST}:{PORT}. Assicurati che 'server.py' sia in esecuzione.")
    except Exception as e:
        print(f"Errore di connessione o socket: {e}")

print("Client spento.")
