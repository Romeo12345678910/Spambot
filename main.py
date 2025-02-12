import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Credenziali API di Telegram
API_ID = 29460099  # Sostituisci con il tuo API_ID
API_HASH = "d6efdf36c51987bbc25de00ef2ef97f6"  # Sostituisci con il tuo API_HASH
SESSION_NAME = "my_userbot"

# Messaggio da inviare
MESSAGE_TEXT = """PRONTO A CHATTARE CON CHIUNQUE TU VOGLIA ANONIMAMENTE⁉️

@AnonimatoChat_bot
@AnonimatoChat_bot
@AnonimatoChat_bot

ti aspettiamo😄✅"""

# Funzione per leggere i link dei gruppi dal file
async def get_group_links():
    """Chiede all'utente i link dei gruppi."""
    group_links = []
    print("Inserisci i link dei gruppi uno per riga. Premi INVIO su una riga vuota per terminare.")
    while True:
        group_link = input("Link gruppo: ").strip()
        if not group_link:
            break
        group_links.append(group_link)
    return group_links

# Funzione per gestire il login e la connessione
async def start_client():
    try:
        # Inizializza il client Telegram
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        await client.start()
        return client
    except SessionPasswordNeededError:
        print("Autenticazione a due fattori richiesta. Inserisci la password.")
        password = input("Password: ")
        await client.start(password=password)
        return client
    except Exception as e:
        print(f"Errore durante l'autenticazione: {e}")
        return None

# Funzione per inviare i messaggi ogni 10 secondi
async def send_messages():
    # Leggi i link dei gruppi dal file
    group_links = await get_group_links()
    if not group_links:
        print("Nessun link trovato.")
        return

    # Avvia il client Telegram
    client = await start_client()
    if not client:
        return  # Se non riesce a connettersi, interrompi

    # Ciclo infinito per inviare il messaggio ogni 10 secondi
    while True:
        for link in group_links:
            try:
                entity = await client.get_entity(link)  # Ottieni il gruppo dal link
                await client.send_message(entity.id, MESSAGE_TEXT)  # Invia il messaggio
                print(f"Messaggio inviato al gruppo: {link}")
            except Exception as e:
                print(f"Errore nell'invio al gruppo {link}: {e}")

        # Aspetta 10 secondi prima di inviare nuovamente il messaggio
        print("Attesa di 10 secondi prima del prossimo invio...")
        await asyncio.sleep(10)  # Pausa di 10 secondi

if __name__ == "__main__":
    asyncio.run(send_messages())
