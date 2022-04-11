import sys
from tkinter import BooleanVar, Button, IntVar, Radiobutton, StringVar, Tk, Canvas, Frame
import time
import random

def read_file(file_name):
    with open(file_name) as f:
        lines = f.read().splitlines()
        return [list(line) for line in lines]


class Board:
    def __init__(self, canvas, board):
        self.board_height = len(board)
        self.board_width = len(board[0])
        self.rect_size = int(500 / max(self.board_height, self.board_width))
        self.rect_colors = [ "#ffffff","#1a1815", "#FC9918"]
        self.board = board
        self.canvas = canvas
        self.next_move_with_shift = False
        self.draw_board()

    def make_iteration(self, sand_mode):
        self.move_pixels()
        self.generate_sand_line(sand_mode)

    def draw_board(self):
        self.image = []
        for i in range(self.board_height):
            self.image.append([])
            for j in range(self.board_width):
                pixel = Pixel(self.canvas, x=j, y=i, size=self.rect_size, color=self.rect_colors[int(self.board[i][j])], is_solid=int(self.board[i][j]) == 1)
                self.image[i].append(pixel)

    def move_pixels(self):
        pixels_already_moved = []
        for row in range(0, self.board_height, 2):
            for col in range(0, self.board_width + 2, 2):
              pixels_already_moved = self.check_chunk(row, col, pixels_already_moved)
              pixels_already_moved = self.check_chunk(row - 1, col - 1, pixels_already_moved)
              pixels_already_moved = self.check_chunk(row, col - 1, pixels_already_moved)
              pixels_already_moved = self.check_chunk(row - 1, col, pixels_already_moved)

    def check_chunk(self, row, col, pixels_already_moved):
        chunk_top = []
        chunk_bot = []
        if row in range(0, self.board_height) and col in range(0, self.board_width):
            chunk_top.append(self.image[row][col])
        if row + 1 in range(0, self.board_height) and col in range(0, self.board_width):
            chunk_bot.append(self.image[row + 1][col])
        if row in range(0, self.board_height) and col + 1 in range(0, self.board_width):
            chunk_top.append(self.image[row][col + 1])
        if row + 1 in range(0, self.board_height) and col + 1 in range(0, self.board_width):
            chunk_bot.append(self.image[row + 1][col + 1])

        for i in range(len(chunk_top)):
            # self.canvas.itemconfig(chunk_top[i].image, fill="#8946A6")
            if len(chunk_bot) != 0 and chunk_top[i].is_sand and (row, col + i) not in pixels_already_moved:
                # Spadanie w dół
                if not chunk_bot[i].is_solid and not chunk_bot[i].is_sand:
                    self.canvas.itemconfig(chunk_top[i].image, fill=self.rect_colors[0])
                    chunk_top[i].is_sand = False
                    self.canvas.itemconfig(chunk_bot[i].image, fill=self.rect_colors[2])
                    chunk_bot[i].is_sand = True
                    pixels_already_moved.append((row + 1, col + i))
                # Spadanie na boki       
                elif len(chunk_top) == 2 and len(chunk_bot) == 2:
                    for j in range(2):
                        is_bot_solid_or_sand = chunk_bot[j].is_sand or chunk_bot[j].is_solid
                        is_neighbour_solid_or_sand = (chunk_top[0].is_sand or chunk_top[0].is_solid) and (chunk_top[1].is_sand or chunk_top[1].is_solid)
                        if not (is_bot_solid_or_sand or is_neighbour_solid_or_sand):
                            self.canvas.itemconfig(chunk_top[i].image, fill=self.rect_colors[0])
                            chunk_top[i].is_sand = False
                            self.canvas.itemconfig(chunk_bot[j].image, fill=self.rect_colors[2])
                            chunk_bot[j].is_sand = True
                            pixels_already_moved.append((row + 1, col + j))
        return pixels_already_moved

    def generate_sand_line(self, mode):
        if mode == "center":
            for i in range(self.board_width // 2 - 1, self.board_width // 2 + 1):
                random_pixel = self.image[0][i]
                random_pixel.is_sand = True
                self.canvas.itemconfig(random_pixel.image, fill=self.rect_colors[2])
        if mode == "random":
            for i in range(random.randrange(1, len(self.board) // 3)):
                random_pixel = self.image[0][random.randrange(0, len(self.board[0]))]
                random_pixel.is_sand = True
                self.canvas.itemconfig(random_pixel.image, fill=self.rect_colors[2])

class Pixel:
    def __init__(self, canvas, x, y, size, color, is_solid=False, is_sand=False):
        self.size = size
        self.canvas = canvas
        self.is_sand = is_sand
        self.is_solid = is_solid
        self.image = self.canvas.create_rectangle(x * size, y * size, x * size + size, y * size + size, fill=color)


def main(filename):
    lines = read_file(filename)
    window = Tk()
    
    canvas = Canvas(window, width=500, height=500)
    canvas.grid(column=0, row=0)
    board = Board(canvas, lines)
    window.update()

    sand_generator_mode = StringVar()
    auto_mode_speed = IntVar()
    auto_on = BooleanVar()

    def make_one_move():
        board.make_iteration(sand_mode=sand_generator_mode.get())
        window.update()

    def start_auto():
        if auto_on.get():
            
            while auto_on.get():
                board.make_iteration(sand_mode=sand_generator_mode.get())
                window.update()
                time.sleep(auto_mode_speed.get() / board.board_height / 10)

    def reset_board():
        board.draw_board()

    buttons = Frame(window, width=500, padx=10, pady=10)
    buttons.grid(column=0, row=1)
    
    R1 = Radiobutton(buttons, text = "Losowe generowanie piasku", variable = sand_generator_mode,
            value = "random", indicator = 0,
            background = "light gray",
            width=35)
    R1.grid(column=1, row=1)
    R1.invoke()

    R2 = Radiobutton(buttons, text = "Generowanie piasku na środku", variable = sand_generator_mode,
            value = "center", indicator = 0,
            background = "light gray",
            width=35)
    R2.grid(column=2, row=1)
    
    R3 = Radiobutton(buttons, text = "Tryb wolny", variable = auto_mode_speed,
        value = 15, indicator = 0,
        background = "light gray",
        width=35)
    R3.grid(column=1, row=2)
    R3.invoke()

    R4 = Radiobutton(buttons, text = "Tryb szybki", variable = auto_mode_speed,
            value = 4, indicator = 0,
            background = "light gray",
            width=35)
    R4.grid(column=2, row=2)

    R5 = Radiobutton(buttons, text = "Start auto", command = start_auto, variable = auto_on,
        value = True, indicator = 0,
        background = "light gray",
        width=35)
    R5.grid(column=1, row=3)

    R6 = Radiobutton(buttons, text = "Stop auto", variable = auto_on,
            value = False, indicator = 0,
            background = "light gray",
            width=35)
    R6.grid(column=2, row=3)
        
    B3 = Button(buttons, text ="Wykonaj jeden ruch", command = make_one_move, width=35)
    B3.grid(column=1, row=4)

    B4 = Button(buttons, text ="Reset", command = reset_board, width=35)
    B4.grid(column=2, row=4)

    window.mainloop()


if __name__ == '__main__':
    main(sys.argv[1])