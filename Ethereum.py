import tkinter as tk
import requests

# Mappa dei caratteri con una matrice LED 5x7
CHAR_MAP = {
    "0": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    "1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ],
    "2": [
        "01110",
        "10001",
        "00001",
        "00110",
        "01000",
        "10000",
        "11111",
    ],
    "3": [
        "01110",
        "10001",
        "00001",
        "00110",
        "00001",
        "10001",
        "01110",
    ],
    "4": [
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010",
    ],
    "5": [
        "11111",
        "10000",
        "11110",
        "00001",
        "00001",
        "10001",
        "01110",
    ],
    "6": [
        "01110",
        "10000",
        "11110",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    "7": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000",
    ],
    "8": [
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110",
    ],
    "9": [
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00001",
        "01110",
    ],
    ".": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00100",
        "00100",
    ],
    "€": [
        "01110",
        "10000",
        "11100",
        "10000",
        "11100",
        "10000",
        "01110",
    ]
}


def on_close(event):
    """Permette di trascinare la finestra."""
    root.geometry(f"+{event.x_root}+{event.y_root}")


def fetch_ethereum_price():
    """Ottiene il prezzo di Ethereum in EUR."""
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=eur")
        data = response.json()
        return f"{data['ethereum']['eur']:.2f}"
    except Exception:
        return "Errore"

def draw_character(canvas, x, y, char, color="green"):
    """Disegna un singolo carattere su una matrice LED."""
    if char not in CHAR_MAP:
        return
    grid = CHAR_MAP[char]
    size = 10  # Dimensione del singolo pallino
    spacing = 2  # Spaziatura tra i pallini
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "1":
                canvas.create_oval(
                    x + j * (size + spacing),
                    y + i * (size + spacing),
                    x + j * (size + spacing) + size,
                    y + i * (size + spacing) + size,
                    fill=color,
                    outline=color,
                )

def update_display():
    """Aggiorna il display con il valore corrente di Ethereum."""
    global canvas
    canvas.delete("all")  # Cancella il contenuto precedente
    price = fetch_ethereum_price()

    # Disegna ogni carattere in sequenza
    x_offset = 10
    for char in price:
        draw_character(canvas, x_offset, 10, char)
        x_offset += 60  # Spaziatura tra i caratteri

    # Aggiorna ogni 5 secondi
    root.after(5000, update_display)

def on_right_click(event):
    """Gestisce il click destro per chiudere il programma."""
    root.quit()

# Configurazione della finestra principale
root = tk.Tk()
root.title("Ethereum LED Timer")

# Rimuovi decorazioni della finestra
root.overrideredirect(True)

# Imposta la trasparenza per Linux
root.attributes("-alpha", 1.0)  # Imposta l'opacità (0.0 completamente trasparente, 1.0 opaco)

# Posiziona la finestra in alto a sinistra dello schermo
root.geometry("450x100+2000+50")
root.configure(bg="#1e1e1e") 

# Imposta la finestra sempre in primo piano
root.attributes("-topmost", True)

# Canvas per i LED
canvas = tk.Canvas(root, width=450, height=100, bg="#1e1e1e", highlightthickness=0)
canvas.pack()

root.bind("<B1-Motion>", on_close)

# Aggiungi l'evento di click destro per chiudere l'app
root.bind("<Button-3>", on_right_click)

# Aggiorna il display inizialmente
update_display()
# Avvia il loop principale
root.mainloop()
