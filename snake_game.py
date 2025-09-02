import tkinter as tk
import random

# Game settings
W, H, SIZE, SPEED = 600, 400, 20, 150
SNAKE_COLOR, BG_COLOR = "#0f0", "#000"
BUBBLE_COLORS = ["red", "blue", "yellow", "purple", "orange", "pink", "cyan"]

class Snake:
    def __init__(self):
        self.coords = [[0, 0] for _ in range(3)]
        self.squares = [canvas.create_rectangle(x, y, x+SIZE, y+SIZE, fill=SNAKE_COLOR) for x, y in self.coords]

class Bubble:
    def __init__(self):
        x, y = random.randint(0, W//SIZE-1)*SIZE, random.randint(0, H//SIZE-1)*SIZE
        self.coords = [x, y]
        self.id = canvas.create_oval(x, y, x+SIZE, y+SIZE, fill=random.choice(BUBBLE_COLORS), tag="food")

def move(snake, food):
    global SPEED
    x, y = snake.coords[0]
    x += SIZE if direction=="right" else -SIZE if direction=="left" else 0
    y += SIZE if direction=="down" else -SIZE if direction=="up" else 0
    snake.coords.insert(0, [x, y])
    snake.squares.insert(0, canvas.create_rectangle(x, y, x+SIZE, y+SIZE, fill=SNAKE_COLOR))

    if [x, y] == food.coords:
        global score
        score += 1
        lbl.config(text=f"Score: {score}")
        canvas.itemconfig(snake.squares[0], fill=random.choice(BUBBLE_COLORS))  # Color effect
        canvas.delete("food"); food = Bubble()
        if score % 5 == 0: SPEED = max(50, SPEED-10)  # Faster every 5 points
    else:
        canvas.delete(snake.squares.pop()); snake.coords.pop()

    if x<0 or x>=W or y<0 or y>=H or [x,y] in snake.coords[1:]:
        return game_over()
    window.after(SPEED, move, snake, food)

def change_dir(d):
    global direction
    if (d=="left" and direction!="right") or (d=="right" and direction!="left") or \
       (d=="up" and direction!="down") or (d=="down" and direction!="up"):
        direction = d

def game_over():
    canvas.delete("all")
    canvas.create_text(W//2, H//2-40, text="GAME OVER", font=("consolas", 40), fill="red")
    canvas.create_text(W//2, H//2, text=f"Score: {score}", font=("consolas", 20), fill="white")
    canvas.create_text(W//2, H//2+40, text="POLDAS AJAY", font=("consolas", 18, "bold"), fill="yellow")
    tk.Button(window, text="Restart", font=("consolas", 14), command=restart).pack(pady=10)

def restart():
    global score, direction, SPEED, snake, food
    score, direction, SPEED = 0, "down", 150
    lbl.config(text="Score: 0")
    for widget in window.pack_slaves():
        if isinstance(widget, tk.Button) and widget["text"] == "Restart": widget.destroy()
    canvas.delete("all")
    snake, food = Snake(), Bubble()
    move(snake, food)

# Main window
window = tk.Tk()
window.title("Snake Bubble Game")
tk.Label(window, text="POLDAS AJAY", font=("consolas", 24, "bold"), fg="red").pack()
lbl = tk.Label(window, text="Score: 0", font=("consolas", 20)); lbl.pack()
canvas = tk.Canvas(window, bg=BG_COLOR, width=W, height=H); canvas.pack()

# Control buttons
frame = tk.Frame(window); frame.pack()
for i, d in enumerate([("↑","up"),("←","left"),("↓","down"),("→","right")]):
    tk.Button(frame, text=d[0], font=("consolas",16), width=4, height=2,
              command=lambda dir=d[1]: change_dir(dir)).grid(row=1 if i else 0, column=i if i else 1)

# Keyboard bindings
for key in ["Left","Right","Up","Down"]:
    window.bind(f'<{key}>', lambda e, k=key.lower(): change_dir(k))

score, direction, snake, food = 0, "down", Snake(), Bubble()
move(snake, food)
window.mainloop()
