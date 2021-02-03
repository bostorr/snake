# --------- Snake v.2 --------- #
# -------- 3 Feb. 2021 -------- #
# ----- by Victor Chalbos ----- #
# ---- works with Python 3 ---- #

from tkinter import *
import random
from PIL import Image, ImageTk

    # --- methods

# move method
def move():
    global tongue,dir,b
    # clear the snake
    for i in range(len(snakebody)):
        can.delete(snakebody[i])
    can.delete(tongue)
    can.delete(gameover)

    # make new snake - tail
    for i in range(len(snakepos)-1,0,-1):
        snakepos[i] = snakepos[i-1]
        snakebody[i] = can.create_rectangle(snakepos[i][0]*wm, snakepos[i][1]*hm, (snakepos[i][0]+1)*wm, (snakepos[i][1]+1)*hm, fill = 'green')

    # make new snake - head
    snakepos[0] = (snakepos[0][0]+dir[0],snakepos[0][1]+dir[1])
    snakebody[0] = can.create_rectangle(snakepos[0][0]*wm, snakepos[0][1]*hm, (snakepos[0][0]+1)*wm, (snakepos[0][1]+1)*hm, fill = 'green')

    if snakepos[0] == apple:
        grow()

    if dir == (0,-1): # tongue up
        tongue = can.create_rectangle(snakepos[0][0]*wm+wm/2-2,snakepos[0][1]*hm-hm/2,snakepos[0][0]*wm+wm/2+2,snakepos[0][1]*hm+2,fill='red')
    elif dir == (0,1): # tongue down
        tongue = can.create_rectangle(snakepos[0][0]*wm+wm/2-2,snakepos[0][1]*hm+hm-4,snakepos[0][0]*wm+wm/2+2,snakepos[0][1]*hm+hm-2+hm/2,fill='red')
    elif dir == (1,0): # tongue right
        tongue = can.create_rectangle(snakepos[0][0]*wm+wm-2,snakepos[0][1]*hm+hm/2-2,snakepos[0][0]*wm+wm-2+wm/2,snakepos[0][1]*hm+hm/2+2,fill='red')
    elif dir == (-1,0): # tongue left
        tongue = can.create_rectangle(snakepos[0][0]*wm+2-wm/2,snakepos[0][1]*hm+hm/2-2,snakepos[0][0]*wm+2,snakepos[0][1]*hm+hm/2+2,fill='red')

    # detects if the snake bites its tail
    for i in range(1,len(snakepos)):
        if snakepos[0] == snakepos[i]:
            lose()

    # detects if the snake's head hits a wall
    if snakepos[0][0] < 0 or snakepos[0][0] >= m or snakepos[0][1] < 0 or snakepos[0][1] >= m:
        lose()

    if b != 0:
        win.after(100,move)


def up(event):
    global dir,b
    dir = (0,-1)
    if b == 0:
        b = 1
        move()

def down(event):
    global dir,b
    dir = (0,1)
    if b == 0:
        b = 1
        move()

def right(event):
    global dir,b
    dir = (1,0)
    if b == 0:
        b = 1
        move()

def left(event):
    global dir,b
    dir = (-1,0)
    if b == 0:
        b = 1
        move()

# growing snake method
def grow():
    global score,apple,redapple
    # increase score
    score += 1
    scoredisp.set(score)

    # redefine apple pos. : random x & y != snake pos.
    # can.delete(apple)
    apple = (random.randint(1,m-2),random.randint(1,m-2))
    while apple == snakepos:
        apple = (random.randint(1,m-2),random.randint(1,m-2))

    # display apple
    can.coords(redapple, apple[0]*wm, apple[1]*hm)

    # grow
    snakepos.append(0)
    snakebody.append(0)
    snakepos[len(snakepos)-1] = (snakepos[len(snakepos)-2][0],snakepos[len(snakepos)-2][1])

# lose method
def lose():
    global score,b,apple,redapple,gameover,tongue
    b = 0
    can.delete(ALL)

    # replace snake
    for i in range(l,len(snakepos)):
        snakepos.pop()
    snakepos[0] = (random.randint(1,m-l),random.randint(1,m-1))
    for i in range(1,l):
        snakepos[i] = (snakepos[i-1][0]+1, snakepos[i-1][1])

    # replace apple
    apple = (random.randint(1,m-2),random.randint(1,m-2))
    while apple == snakepos:
        apple = (random.randint(1,m-2),random.randint(1,m-2))

    # display snake
    for i in range(len(snakepos)):
        snakebody[i] = can.create_rectangle(snakepos[i][0]*wm, snakepos[i][1]*hm, (snakepos[i][0]+1)*wm, (snakepos[i][1]+1)*hm, fill = 'green')
    # display tongue
    tongue = can.create_rectangle(snakepos[0][0]*wm+2-wm/2,snakepos[0][1]*hm+hm/2-2,snakepos[0][0]*wm+2,snakepos[0][1]*hm+hm/2+2,fill='red')

    # display apple
    redapple = can.create_image(apple[0]*wm, apple[1]*hm,image=applephoto,anchor='nw')

    # GAME OVER message
    f = open('highestscore.txt', mode='r')
    high = int(f.read())
    f.close()
    if score > high:
        f = open('highestscore.txt', mode='w')
        f.write(str(score))
        f.close()
    gameover = can.create_text(w/2,hm,justify='center',text='GAME OVER\nYour score was : '+str(score))

    f = open('highestscore.txt', mode='r')
    high = int(f.read())
    f.close()

    score = 0
    scoredisp.set(score)
    highscoredisp.set(high)

# ---------------------------------------------------------------------------- #

    # -- init

dir = (0,0)
b = 0 # b allows to move() in a loop until another key is pressed
m = 20 # the window will be a 2D array m * m
l = 2 # the init value of snake length
score = 0 # initial score

# init snake position
snakepos = [] # the position of each square of the snake
    # snakepos : list
    # snakepos[i] : tuple (X,Y)
    # snakepos[0] : the head
snakebody = [] # the graphic squares for each position
    # snakebody[i] is the square at the position snakepos[i]

for i in range(l): # the snake starts at the size l
    snakepos.append(0)
    snakebody.append(0)
# its head is placed randomly
snakepos[0] = (random.randint(1,m-l),random.randint(1,m-1))
# its tail follows its head on the right
for i in range(1,l):
    snakepos[i] = (snakepos[i-1][0]+1, snakepos[i-1][1])

# init apple position
apple = (random.randint(1,m-2),random.randint(1,m-2))
while apple == snakepos: # the apple must not be placed on the head
    apple = (random.randint(1,m-2),random.randint(1,m-2))

    # -- display

w = 700 # canvas width
h = 700 # canvas height
wm = w/m # width of an array cell
hm = h/m # height of an array cell

# window and canvas
win = Tk()
# can is the play area
can = Canvas(win, width = w, height = h , bg = 'palegreen')
can.grid(row=1,column=0)
gameover = can.create_text(0,0) # not important, just to give the first move() something to delete in line 19

# display snake
for i in range(len(snakepos)):
    snakebody[i] = can.create_rectangle(snakepos[i][0]*wm, snakepos[i][1]*hm, (snakepos[i][0]+1)*wm, (snakepos[i][1]+1)*hm, fill = 'green')

# little feature : a tongue in front of the head
tongue = can.create_rectangle(snakepos[0][0]*wm+2-wm/2,snakepos[0][1]*hm+hm/2-2,snakepos[0][0]*wm+2,snakepos[0][1]*hm+hm/2+2,fill='red')

# display apple
path = "img/apple.png"
appleimg = Image.open(path).resize((int(wm),int(hm)),Image.ANTIALIAS)
applephoto = ImageTk.PhotoImage(appleimg)
redapple = can.create_image(apple[0]*wm, apple[1]*hm,image=applephoto,anchor='nw')
# display trophy
path = "img/trophy.png"
trophyimg = Image.open(path).resize((int(wm),int(hm)),Image.ANTIALIAS)
trophy = ImageTk.PhotoImage(trophyimg)

# info is the canvas that displays the score
info = Canvas(win, width = w, height = h/10)
info.grid(row=0,column=0,columnspan=4)
Label(info, image=applephoto).grid(row=0,column=0)
scoredisp = StringVar()
Label(info, textvariable=scoredisp, font = ("Arial",20)).grid(row=0,column=1)
scoredisp.set('0')

# carry the highest score
f = open('highestscore.txt', mode='r')
high = f.read()
f.close()
Label(info, image=trophy).grid(row=0,column=2)
highscoredisp = StringVar()
highscoredisp.set(high)
Label(info, textvariable=highscoredisp, font = ("Arial",20)).grid(row=0,column=3)

# bind the keys to the methods
can.bind_all('<Up>',up)
can.bind_all('<Down>',down)
can.bind_all('<Right>',right)
can.bind_all('<Left>',left)

win.mainloop()
