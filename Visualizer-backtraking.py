# Import modul pygame dan mengatur beberapa konstanta
import pygame
from turtle import width
WIDTH = 600
ROW = 4
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('N-Queen VIsualizer')

# Mendefinisikan beberapa warna
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

# Membuat kelas Spot untuk merepresentasikan setiap sel di papan catur
# Spot memiliki properti seperti warna, posisi, dll.


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.total_row = total_rows
        self.width = width
        self.color = WHITE
        self.x = row*width
        self.y = col*width

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_current(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_checking(self):
        return self.color == BLUE

    def is_reset(self):
        return self.color == WHITE

    def make_closed(self):
        self.color = RED

    def make_current(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_checking(self):
        self.color = BLUE

    def make_reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

# Fungsi `algorithm` adalah pintasan untuk memanggil `solveNQueen` dan menampilkan hasilnya


def algorithm(grid):
    sol = solveNQueen(lambda: draw(WIN, grid, ROW, WIDTH), grid, 0)
    if sol:
        print("Solution Found")
        return True
    else:
        print("Solution Not Found")
        return False

# Fungsi `isSafe` memeriksa apakah tempat di (row, col) aman untuk menempatkan ratu


def isSafe(draw, grid, row, col):
    temp = grid[row][col].color
    grid[row][col].make_current()
    draw()
    for i in range(col):
        if grid[row][i].is_barrier():
            grid[row][i].make_closed()
            draw()
            grid[row][i].make_barrier()
            draw()
            for j in range(col):
                if i == j:
                    continue
                grid[row][j].make_reset()
            grid[row][col].make_reset()
            return False
        if not grid[row][i].is_current():
            grid[row][i].make_checking()
            draw()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_checking():
                grid[i][j].make_reset()

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if grid[i][j].is_barrier():
            grid[i][j].make_closed()
            draw()
            grid[i][j].make_barrier()
            draw()
            for i1, j1 in zip(range(row, -1, -1), range(col, -1, -1)):
                if i1 == i and j1 == j:
                    continue
                grid[i1][j1].make_reset()
            grid[row][col].make_reset()
            return False
        if not grid[i][j].is_current():
            grid[i][j].make_checking()
            draw()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_checking():
                grid[i][j].make_reset()

    for i, j in zip(range(row, ROW, 1), range(col, -1, -1)):
        if grid[i][j].is_barrier():
            grid[i][j].make_closed()
            draw()
            grid[i][j].make_barrier()
            draw()
            for i1, j1 in zip(range(row, ROW, 1), range(col, -1, -1)):
                if i1 == i and j1 == j:
                    continue
                grid[i1][j1].make_reset()
            grid[row][col].make_reset()
            return False
        if not grid[i][j].is_current():
            grid[i][j].make_checking()
            draw()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_checking():
                grid[i][j].make_reset()
        grid[row][col].color = temp
        return True

# Fungsi `solveNQueen` adalah implementasi utama dari algoritma backtracking


def solveNQueen(draw, grid, col):
    if col > ROW:
        return True
    for i in range(ROW):
        if isSafe(draw, grid, i, col):
            grid[i][col].make_barrier()
            draw()
            if solveNQueen(draw, grid, col+1) == True:
                return True

            grid[i][col].make_reset()
            draw()
    return False

# Fungsi `make_grid` membuat papan grid ROWxROW dengan sel-sel Spot


def make_grid(rows, width):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

# Fungsi `draw_grid` menggambar garis-garis di antara sel-sel Spot


def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

# Fungsi `draw` menggambar seluruh papan dan grid di layar


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)

    pygame.display.flip()
    # pygame.time.wait(200)

# Fungsi `main` adalah titik masuk utama program


def main(win, width):
    grid = make_grid(ROW, width)
    run = True
    started = False

    while run:
        draw(win, grid, ROW, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                started = True
                algorithm(grid)
    pygame.quit()


# Memanggil fungsi `main` untuk memulai program
main(WIN, WIDTH)
