from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 150
SPACE_SIZE = 50 # size of each object on the game
BODY_PARTS = 3
SNACK_COLOR = "#3D8D7A"
FOOD_COLOR = "#FBFFE4"
BACKGROUND_COLOR = "#B3D8A8"

class Snack:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0]) #append new list and the coordinates for each body part at the start of the game will be 0, 0 so that our snack will appear in the top left corner
        # creating some squares
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNACK_COLOR, tags="Snack")
            self.squares.append(square)


class Food:
    def __init__(self):   #this will create food obj for us
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE  #GAME_WIDTH IS 700 & SPACE_SIZE is 50, so there will 700/50 = 14 possible blocks
                                                                            # to conver it in pixel, we've multiply it with space_size
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE # SAME

        self.coordinates = [x, y] # list of x and y

        # we need to draw our food obj on canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="FOOD")



def next_turn(snack, food):
    x, y = snack.coordinates[0]  # head of the snack
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Update coordinates of the head of the snack
    snack.coordinates.insert(0, (x, y))
    # New graphic for the head of the snack square
    squares = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNACK_COLOR)
    # Update snack list of squares
    snack.squares.insert(0, squares)

    if x == food.coordinates[0] and y == food.coordinates[1]:  # They are overlapping
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("FOOD")  # ✅ Fix: Correct tag for deleting the food object
        food = Food()  # ✅ Creating a new food object
    else:
        # We will only delete the last body part of our snack if we don't eat a food object
        del snack.coordinates[-1]
        canvas.delete(snack.squares[-1])
        del snack.squares[-1]

    if check_collisions(snack):
        game_over()
    else:
        window.after(SPEED, next_turn, snack, food)

def change_direction(new_direction):

    global direction # this is the old directio

    if new_direction == 'left':
        if direction != 'right': # old direction is not right because we dont want to go backward and do a 180 degree turn
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left': # old direction is not right because we dont want to go backward and do a 180 degree turn
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down': # old direction is not right because we dont want to go backward and do a 180 degree turn
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up': # old direction is not right because we dont want to go backward and do a 180 degree turn
            direction = new_direction


def check_collisions(snack):
    x, y = snack.coordinates[0]

    # check to see if we cross the left or right border of the game
    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_WIDTH:
        return True
    # if snack touches its tail or another body part
    for body_part in snack.coordinates[1:]: # we are going to set this everything after the head of the snack
        # we are going to check see if any of the coordinates are matching
        if x == body_part[0] and y == body_part[1]:
            print("Game over")
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="game over")


window = Tk()
window.title("Snack Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text=f"Score: {score}", font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snack = Snack()
food = Food()


next_turn(snack, food)

window.mainloop()
