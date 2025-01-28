import tkinter as tk
import csv

class ScalableMapDrawer(tk.Frame):
    def __init__(self, master=None, rows=20, cols=20, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = rows
        self.cols = cols
        
        # Dwuwymiarowa tablica przechowująca wartości 0/1
        self.map_data = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # Zmienna do przechowywania aktualnych wymiarów Canvas
        # (będą uaktualniane przy każdym resize)
        self.canvas_width = 1
        self.canvas_height = 1
        
        # Tworzymy widget Canvas i pozwalamy mu się rozciągać w obie strony
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(expand=True, fill="both")
        
        # Obsługa kliknięcia myszą
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Obsługa zmiany rozmiaru (zdarzenie <Configure>)
        self.canvas.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """
        Wywoływane automatycznie, gdy Canvas zmienia rozmiar
        (np. gdy użytkownik powiększa lub pomniejsza okno).
        """
        # Zapamiętujemy nowe wymiary Canvas
        self.canvas_width = event.width
        self.canvas_height = event.height
        
        # Rysujemy mapę ponownie przy uwzględnieniu nowych wymiarów
        self.draw_map()

    def draw_map(self):
        """
        Rysuje wszystkie komórki na Canvas, dopasowując je do aktualnych wymiarów.
        """
        self.canvas.delete("all")  # Usunięcie starych rysunków
        
        if self.rows == 0 or self.cols == 0:
            return
        
        # Obliczamy rozmiar komórki (może być "prostokątna", jeśli okno ma inny ratio)
        cell_width = self.canvas_width / self.cols
        cell_height = self.canvas_height / self.rows
        
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * cell_width
                y1 = r * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                
                # Wybór koloru w zależności od wartości 0 (biały) lub 1 (czarny)
                color = "black" if self.map_data[r][c] == 1 else "white"
                
                # Rysujemy prostokąt reprezentujący komórkę
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def on_click(self, event):
        """
        Obsługa kliknięcia myszy – zmiana wartości w odpowiedniej komórce.
        """
        # Obliczamy rozmiar komórki na podstawie aktualnych wymiarów
        cell_width = self.canvas_width / self.cols
        cell_height = self.canvas_height / self.rows
        
        # Wyliczamy indeks kolumny i wiersza z event.x / event.y
        col = int(event.x // cell_width)
        row = int(event.y // cell_height)
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            # Zmieniamy 0 na 1, 1 na 0
            self.map_data[row][col] = 1 - self.map_data[row][col]
            # Przerysowujemy mapę po zmianie
            self.draw_map()

    def save_map_to_file(self, filename):
        """
        Zapisuje obecną zawartość mapy do pliku CSV.
        """
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for row_data in self.map_data:
                writer.writerow(row_data)
        print(f"Mapa została zapisana do pliku: {filename}")

def main():
    root = tk.Tk()
    root.title("Skalowalna Mapa (0/1)")

    # Inicjujemy nasz panel rysujący z domyślną liczbą wierszy i kolumn
    app = ScalableMapDrawer(root, rows=64, cols=64)
    app.pack(expand=True, fill="both")

    # Dodajemy przycisk do zapisywania mapy
    btn_save = tk.Button(root, text="Zapisz", command=lambda: app.save_map_to_file("map.csv"))
    btn_save.pack()

    # Uruchamiamy pętlę zdarzeń
    root.mainloop()

if __name__ == "__main__":
    main()
