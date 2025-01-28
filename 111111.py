import pygame
import sys

def main():
    pygame.init()

    # Pobierz informację o rozdzielczości ekranu
    info_object = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info_object.current_w, info_object.current_h
    
    # Ustaw tryb pełnoekranowy
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mapa 0 i 1 - pędzle + zapis binarny do pliku tekstowego")
    
    # Parametry mapy (siatki)
    GRID_ROWS = 64  # liczba wierszy
    GRID_COLS = 64  # liczba kolumn
    
    # Obliczamy rozmiary kafelków
    tile_width = SCREEN_WIDTH // GRID_COLS
    tile_height = SCREEN_HEIGHT // GRID_ROWS
    
    # Dwuwymiarowa lista - wartości początkowe to 0
    grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    
    # Rozmiar pędzla (domyślnie 1x1)
    brush_size = 1
    
    # Funkcja rysująca siatkę
    def draw_grid():
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                color = (255, 255, 255) if grid[row][col] == 1 else (30, 30, 30)
                rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                pygame.draw.rect(screen, color, rect)
                # Możesz odkomentować tę linię, aby rysować linie siatki:
                # pygame.draw.rect(screen, (50, 50, 50), rect, 1)
    
    # Funkcja, która "maluje" kafle w zależności od rozmiaru pędzla
    def paint_tiles(center_row, center_col, value):
        # Wyliczamy offset, żeby malować kwadrat brush_size x brush_size
        offset = brush_size // 2
        
        for r in range(center_row - offset, center_row + offset + 1):
            for c in range(center_col - offset, center_col + offset + 1):
                # Upewniamy się, że nie wychodzimy poza siatkę
                if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
                    grid[r][c] = value
    
    # Funkcja do zapisu siatki do pliku w formacie „binarny tekst”
    # Każda linia to jeden wiersz siatki (ciąg znaków 0/1).
    def save_to_file_txt(filename="map.txt"):
        with open(filename, "w") as f:
            for row in grid:
                line = "".join(str(cell) for cell in row)
                f.write(line + "\n")
        print(f"Zapisano aktualny stan mapy do pliku: {filename}")
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Zmiana rozmiaru pędzla
                elif event.key == pygame.K_1:
                    brush_size = 1
                elif event.key == pygame.K_3:
                    brush_size = 3
                elif event.key == pygame.K_5:
                    brush_size = 5
                # Zapis do pliku (klawisz S)
                elif event.key == pygame.K_s:
                    save_to_file_txt("map.txt")
        
        # Sprawdzamy przyciski myszy (lewym: maluj 1, prawym: maluj 0)
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] or mouse_buttons[2]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Obliczamy, w którym kaflu się znajdujemy
            col = mouse_x // tile_width
            row = mouse_y // tile_height
            
            # Malujemy
            if mouse_buttons[0]:
                paint_tiles(row, col, 1)  # Lewy przycisk -> 1
            elif mouse_buttons[2]:
                paint_tiles(row, col, 0)  # Prawy przycisk -> 0
        
        # Rysujemy siatkę
        screen.fill((0, 0, 0))
        draw_grid()
        
        # Aktualizujemy ekran
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
