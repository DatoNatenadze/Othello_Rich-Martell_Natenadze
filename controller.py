from model import *
from tkinter import *

def handle_mouse(event, args):
    root = args['root']
    global RUNNING
    global CHOOSING
    global VSAI
    screen = args['screen']
    mixer = args['mixer']
    depth = args['depth']
    xMouse = event.x
    yMouse = event.y
    if CHOOSING:
        if event.widget.find_withtag("current"):
            current_tags = event.widget.gettags("current")
            if "AI" in current_tags:
                CHOOSING=False
                VSAI = True
                run_AI(screen)
            elif "Player" in current_tags:
                CHOOSING=False
                play_game(screen, mixer, depth, VSAI)
    elif RUNNING:
        if xMouse>=450 and yMouse<=50:
            root.destroy()
        elif xMouse<=50 and yMouse<=50:
            play_game(screen, mixer, depth, VSAI)
        else:
            if VSAI:
                if board.player==0:
                    x = int((event.x-50)/50)
                    y = int((event.y-50)/50)
                    if 0<=x<=7 and 0<=y<=7:
                        if ModelHelper.check_move(board.array,board.player,x,y):
                            board.board_move(x,y, board, VSAI, mixer, screen, depth)
            else:
                if board.player==0:
                    x = int((event.x-50)/50)
                    y = int((event.y-50)/50)
                    if 0<=x<=7 and 0<=y<=7:
                        if ModelHelper.check_move(board.array,board.player,x,y):
                            board.board_move(x,y, board, VSAI, mixer, screen, depth)
                if board.player==1:
                    x = int((event.x-50)/50)
                    y = int((event.y-50)/50)
                    if 0<=x<=7 and 0<=y<=7:
                        if ModelHelper.check_move(board.array,board.player,x,y):
                            board.board_move(x,y, board, VSAI, mixer, screen, depth)
    else:	
        if 300<=yMouse<=350:
            if 25<=xMouse<=155:
                depth = 1
                play_game(screen, mixer, depth, VSAI)
            elif 180<=xMouse<=310:
                depth = 4
                play_game(screen, mixer, depth, VSAI)
            elif 335<=xMouse<=465:
                depth = 6
                play_game(screen, mixer, depth, VSAI)

def key_handling(event, args):
    root = args['root']
    screen = args['screen']
    mixer = args['mixer']
    symbol = event.keysym
    if symbol.lower()=="r":
        play_game(screen, mixer)
    elif symbol.lower()=="q":
        root.destroy()

def create_buttons(screen):
        WHITE = "white"

        screen.create_rectangle(0,5,50,55,fill="#fa0202", outline="#000033")
        screen.create_rectangle(0,0,50,50,fill="#fa0202", outline="#000088")

        screen.create_arc(5,5,45,45,fill="#000088", width="2",style="arc",outline=WHITE,extent=300)
        screen.create_polygon(33,38,36,45,40,39,fill=WHITE,outline=WHITE)

        DARK_RED = "#330000"
        MEDIUM_RED = "#880000"
        screen.create_rectangle(450, 5, 500, 55, fill=DARK_RED, outline=DARK_RED)
        screen.create_rectangle(450, 0, 500, 50, fill=MEDIUM_RED, outline=MEDIUM_RED)
        screen.create_line(455, 5, 495, 45, fill=WHITE, width=3)
        screen.create_line(495, 5, 455, 45, fill=WHITE, width=3)
    
def run_AI(screen):
    screen.delete(ALL)
    for i in range(3):
        screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
        screen.create_rectangle(25+155*i, 300, 155+155*i, 350, fill="#111", outline="#111")

        spacing = 130/(i+2)
        for x in range(i+1):
            screen.create_text(25+(x+1)*spacing+155*i,326,anchor="c",text="\u2605", font=("Consolas", 25),fill="#b29600")
            screen.create_text(25+(x+1)*spacing+155*i,327,anchor="c",text="\u2605", font=("Consolas",25),fill="#b29600")
            screen.create_text(25+(x+1)*spacing+155*i,325,anchor="c",text="\u2605", font=("Consolas", 25),fill="#ffd700")
    screen.update()

def choose_style(screen):
    screen.create_text(50, 10, anchor="c",text="Pau Rich-Martel",font=("Consolas", 10),fill="red")
    screen.create_text(50, 20, anchor="c",text="Davit Natenadze",font=("Consolas", 10),fill="red")
    screen.create_text(250,203,anchor="c",text="Othello",font=("Consolas", 50),fill="#aaa")
    screen.create_text(250,200,anchor="c",text="Othello",font=("Consolas", 50),fill="#fff")
    screen.create_text(0,325,anchor="c",text="VS AI", font=("Consolas",25),fill="#b29600", tags="AI")
    screen.create_text(400,325,anchor="c",text="VS Player", font=("Consolas", 25),fill="#ffd700", tags="Player")

    screen.update()


def play_game(screen, mixer, depth, VSAI):
    global board, RUNNING
    RUNNING = True
    screen.delete(ALL)
    create_buttons(screen)
    board = 0

    ModelHelper.grid_background(screen)

    board = Board(screen, mixer)
    board.update(screen, depth, VSAI, board, mixer)