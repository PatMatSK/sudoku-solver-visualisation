import tkinter as tk
from tkinter import filedialog

OFFSET = 5
SQUARE_SIZE = 50
GRID_SIZE = 9 * SQUARE_SIZE
TIME_OUT = 10
root = tk.Tk()
root.title("Sudoku")
canvas = tk.Canvas(root, width=GRID_SIZE+2*OFFSET, height=GRID_SIZE+2*OFFSET)
canvas.pack()
data = []
numbers = []


def initiate_grid():
    for i in range(0, GRID_SIZE + SQUARE_SIZE, SQUARE_SIZE):  # to also draw last line
        canvas.create_line(OFFSET, i+OFFSET, GRID_SIZE+OFFSET, i+OFFSET)
        canvas.create_line(i+OFFSET, OFFSET, i+OFFSET, GRID_SIZE+OFFSET)


def clean():
    global numbers
    for row in numbers:
        for num in row:
            canvas.delete(num)
    canvas.update()
    numbers = []


def get_data():
    global data, numbers
    clean()
    file_name = filedialog.askopenfilename(parent=root, title="Choose file", filetypes=[("Txt files", "*.txt")])
    if file_name == "":
        return False
    file = open(file_name, "r")
    input_data = file.read().split("\n")
    file.close()
    return input_data


def set_data():
    global data, numbers
    input_data = get_data()
    if not input_data:
        return

    numbers, data = [], []
    y = OFFSET + SQUARE_SIZE/2

    for i in input_data:
        data_row, can_row = [], []
        x = OFFSET + SQUARE_SIZE/2
        for s in i.split():
            data_row.append(int(s))
            if s == "0":
                s = ""
            can_row.append(canvas.create_text(x, y, text=str(s), font=("Purisa", 12)))
            x += SQUARE_SIZE
        data.append(data_row)
        numbers.append(can_row)
        y += SQUARE_SIZE

    canvas.update()


def check(row, column, number):
    if number in data[row]:
        return False
    for s in data:
        if s[column] == number:
            return False
    y = (row // 3) * 3
    x = (column // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if number == data[y + i][x + j]:
                return False
    return True


def edit(x, y, val):
    global data
    data[y][x] = val
    if val == 0:
        val = ""
    canvas.itemconfig(numbers[y][x], text=str(val), fill='red')
    canvas.after(TIME_OUT)
    canvas.update()


def solve_sudoku():
    global data
    for y in range(0, 9):
        for x in range(0, 9):
            if data[y][x] == 0:
                for number in range(1, 10):
                    if check(y, x, number):
                        edit(x, y, number)
                        if solve_sudoku():
                            return True
                        edit(x, y, 0)

                return False
    return True


def solve_manager():
    if not data:
        return
    load_button["state"] = "disabled"
    solve_button["state"] = "disabled"
    solve_sudoku()
    load_button["state"] = "normal"
    solve_button["state"] = "normal"


initiate_grid()

load_button = tk.Button(root, text="load sudoku", command=set_data)
load_button.pack()
solve_button = tk.Button(root, text="SOLVE", command=solve_manager)
solve_button.pack()

root.mainloop()
