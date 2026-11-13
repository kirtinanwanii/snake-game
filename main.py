from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 40
BODY_PARTS = 3

BAR_COLOR = "#14111f"
GRID_COLOR_1 = "#1f1d2e"
GRID_COLOR_2 = "#1b1929"
HEAD_COLOR = "#ebbcba"
SNAKE_COLOR = "#c4a7e7"
FOOD_COLOR = "#f6c177"
TEXT_COLOR = "#e0def4"
DANGER_COLOR = "#eb6f92"
PAD = 3  

OPPOSITES = {"up": "down", "down": "up", "left": "right", "right": "left"}


class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []

        start_x = (GAME_WIDTH // SPACE_SIZE // 2) * SPACE_SIZE
        start_y = (GAME_HEIGHT // SPACE_SIZE // 2) * SPACE_SIZE

        for i in range(BODY_PARTS):
            self.coordinates.append((start_x - i * SPACE_SIZE, start_y))

        for i in range(BODY_PARTS):
            x, y = self.coordinates[i]
            if i == 0:
                self.squares.append(draw_square(x, y, HEAD_COLOR))
            else:
                self.squares.append(draw_square(x, y, SNAKE_COLOR))


class Food:
    def __init__(self, snake):
        
        while True:
            x = random.randint(0, GAME_WIDTH // SPACE_SIZE - 1) * SPACE_SIZE
            y = random.randint(0, GAME_HEIGHT // SPACE_SIZE - 1) * SPACE_SIZE

            on_snake = False
            for part in snake.coordinates:
                if part == (x, y):
                    on_snake = True

            if not on_snake:
                break

        self.coordinates = (x, y)
        canvas.create_oval(x + 6, y + 6, x + SPACE_SIZE - 6, y + SPACE_SIZE - 6, fill=FOOD_COLOR, outline="", tag="food")


def draw_square(x, y, color):
    return canvas.create_rectangle(x + PAD, y + PAD, x + SPACE_SIZE - PAD, y + SPACE_SIZE - PAD,fill=color, outline="", tag="snake")


def draw_grid():
    for row in range(GAME_HEIGHT // SPACE_SIZE):
        for col in range(GAME_WIDTH // SPACE_SIZE):
            if (row + col) % 2 == 0:
                color = GRID_COLOR_1
            else:
                color = GRID_COLOR_2
            x = col * SPACE_SIZE
            y = row * SPACE_SIZE
            canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, outline="")


def update_label():
    label.config(text="Score: {}     Best: {}".format(score, high_score))


def next_turn(snake, food):
    global direction, score, high_score

    if paused:
        window.after(SPEED, next_turn, snake, food)
        return

    direction = next_direction
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    
    canvas.itemconfig(snake.squares[0], fill=SNAKE_COLOR)
    snake.coordinates.insert(0, (x, y))
    snake.squares.insert(0, draw_square(x, y, HEAD_COLOR))

    if (x, y) == food.coordinates:
        score += 1
        if score > high_score:
            high_score = score
        update_label()
        canvas.delete("food")
        food = Food(snake)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_directions(new_direction):
    global next_direction

   
    if new_direction != OPPOSITES[direction]:
        next_direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    global game_running
    game_running = False

    cx = GAME_WIDTH / 2
    cy = GAME_HEIGHT / 2

    canvas.create_rectangle(cx - 250, cy - 110, cx + 250, cy + 110,
                            fill=BAR_COLOR, outline=HEAD_COLOR, width=3)
    canvas.create_text(cx, cy - 50, font=('consolas', 50, 'bold'), text="GAME OVER", fill=DANGER_COLOR)
    canvas.create_text(cx, cy + 10, font=('consolas', 24),
                       text="Score: {}   Best: {}".format(score, high_score), fill=TEXT_COLOR)
    canvas.create_text(cx, cy + 65, font=('consolas', 18), text="Press R to restart", fill=HEAD_COLOR)


def toggle_pause():
    global paused

    if not game_running:
        return

    paused = not paused
    if paused:
        canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, font=('consolas', 60, 'bold'),
                           text="PAUSED", fill=TEXT_COLOR, tag="pause")
    else:
        canvas.delete("pause")


def start_game():
    global snake, food, score, direction, next_direction, paused, game_running

    canvas.delete(ALL)
    draw_grid()

    score = 0
    direction = "right"
    next_direction = "right"
    paused = False
    game_running = True
    update_label()

    snake = Snake()
    food = Food(snake)
    next_turn(snake, food)


def restart():
    if not game_running:
        start_game()


window = Tk()
window.title("THE SNAKE GAME")
window.resizable(False, False)
window.config(bg=BAR_COLOR)

score = 0
high_score = 0
direction = "right"
next_direction = "right"
paused = False
game_running = False

label = Label(window, text="", font=('consolas', 28, 'bold'), bg=BAR_COLOR, fg=TEXT_COLOR, pady=8)
label.pack(fill=X)

canvas = Canvas(window, bg=GRID_COLOR_2, height=GAME_HEIGHT, width=GAME_WIDTH, highlightthickness=0)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_directions('left'))
window.bind('<Right>', lambda event: change_directions('right'))
window.bind('<Up>', lambda event: change_directions('up'))
window.bind('<Down>', lambda event: change_directions('down'))
window.bind('<a>', lambda event: change_directions('left'))
window.bind('<d>', lambda event: change_directions('right'))
window.bind('<w>', lambda event: change_directions('up'))
window.bind('<s>', lambda event: change_directions('down'))
window.bind('<p>', lambda event: toggle_pause())
window.bind('<space>', lambda event: toggle_pause())
window.bind('<r>', lambda event: restart())

window.focus_force()
start_game()

window.mainloop()