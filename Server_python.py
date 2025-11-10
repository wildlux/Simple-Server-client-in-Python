# server.py
import socket
import config

HOST = config.HOST_IP
PORT = config.PORTA_SERVER

print(f"Server configurato su {HOST}:{PORT}")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Permette il riutilizzo della porta (fondamentale per lo sviluppo)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((HOST, PORT))
        s.listen()
        print("Server in ascolto. In attesa di connessioni... (Ctrl+C per spegnere)")

        # CICLO ESTERNO: Mantiene il server attivo
        while True:
            # Si blocca in attesa di una NUOVA connessione
            conn, addr = s.accept()

            with conn:
                print(f"\n--- Nuova connessione da {addr} ---")

                # CICLO INTERNO: Gestisce la comunicazione con il client ATTUALE
                while True:
                    try:
                        # Riceve dati
                        data = conn.recv(1024)
                    except ConnectionResetError:
                        print(f"Connessione con {addr} resettata bruscamente.")
                        break

                    if not data:
                        print(f"Connessione chiusa da {addr}.")
                        break

                    comando = data.decode('utf-8').strip().upper()
                    print(f"Comando ricevuto da {addr}: '{comando}'")

                    # Logica del Server
                    if comando == "MUSICA":
                        messaggio_risposta = "OK_MUSICA"
                    elif comando == "MESSAGGIO":
                        messaggio_risposta = "OK_MESSAGGIO"
                    elif comando == "CIAO":
                        messaggio_risposta = "A presto! Disconnessione."
                        conn.sendall(messaggio_risposta.encode('utf-8'))
                        break
                    else:
                        messaggio_risposta = f"Comando '{comando}' non riconosciuto."

                    # Invia la risposta al client
                    conn.sendall(messaggio_risposta.encode('utf-8'))

            print(f"--- Connessione con {addr} terminata. In attesa del prossimo client... ---")

except KeyboardInterrupt:
    print("\nServer spento manualmente (Ctrl+C).")
except Exception as e:
    print(f"Si è verificato un errore critico: {e}")
