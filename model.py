from time import *
from model_helper import ModelHelper
from random import *
import os
import sys
VSAI = False
RUNNING = False
CHOOSING = True
nodes = 0
depth = 4
moves = 0
class Sounds:
    def play_background(mixer):
        # mixer.Channel(0).play(mixer.Sound(resource_path('background.wav')), loops=-1)
        mixer.Channel(0).play(mixer.Sound(('resources/sounds/background.wav')), loops=-1)
        mixer.Channel(0).set_volume(0.2)
    def play_move(mixer):
        # mixer.Channel(1).play(mixer.Sound(resource_path('move.wav')), loops=-1)
        mixer.Channel(1).play(mixer.Sound(('resources/sounds/move.wav')))
class Board:
    def __init__(self, *args):
        screen = args[0]
        mixer = args[1]
        screen.configure(bg='green')
        self.player = 0
        self.passed = False
        self.won = False
        self.array = []
        for x in range(8):
            self.array.append([])
            for y in range(8):
                self.array[x].append(None)

        self.array[3][3]="w"
        self.array[3][4]="b"
        self.array[4][3]="b"
        self.array[4][4]="w"

        self.oldarray = self.array
        Sounds.play_background(mixer)
    def update(self, screen, depth, VSAI, board, mixer):
        screen.delete("highlight")
        screen.delete("tile")
        for x in range(8):
            for y in range(8):
                if self.oldarray[x][y]=="w":
                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")

                elif self.oldarray[x][y]=="b":
                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
        screen.update()
        for x in range(8):
            for y in range(8):
                if self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="w":
                    screen.delete("{0}-{1}".format(x,y))
                    for i in range(21):
                        screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
                        screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
                        if i%3==0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    for i in reversed(range(21)):
                        screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
                        screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
                        if i%3==0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#aaa",outline="#aaa")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#fff",outline="#fff")
                    screen.update()

                elif self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="b":
                    screen.delete("{0}-{1}".format(x,y))
                    for i in range(21):
                        screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
                        screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
                        if i%3==0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    for i in reversed(range(21)):
                        screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
                        screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
                        if i%3==0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")

                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#000",outline="#000")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#111",outline="#111")
                    screen.update()
        for x in range(8):
            for y in range(8):
                    if self.player == 0:
                        if ModelHelper.check_move(self.array,self.player,x,y):
                            screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="#FFFFFF",outline="#FFFFFF")
                    if VSAI==False:
                        if self.player == 1:
                            if ModelHelper.check_move(self.array,self.player,x,y):
                                screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="#000000",outline="#000000")
        if not self.won:
            self.draw_score_board(screen)
            if VSAI==True:
                if self.player==1:
                    screen.create_text(260, 17, text="AI is thinking", tags=("thinking"),font=("Consolas",27),fill="red")
                    screen.update()
                    startTime = time()
                    self.oldarray = self.array
                    alphaBetaResult = self.alphaBeta(self.array,depth,-float("inf"),float("inf"),1, board)
                    self.array = alphaBetaResult[1]
                    if len(alphaBetaResult)==3:
                        position = alphaBetaResult[2]
                        self.oldarray[position[0]][position[1]]="b"
                    self.player = 1-self.player
                    deltaTime = round((time()-startTime)*100)/100
                    if deltaTime<2:
                        sleep(2-deltaTime)
                    nodes = 0
                    self.pass_test(screen, depth, board, mixer)
                    screen.delete("thinking")
                    Sounds.play_move(mixer)
                    self.update(screen, depth, VSAI, board, mixer)
        else:
            self.check_win(screen)

    def board_move(self,x,y, board, VSAI, mixer, screen, depth):
        global nodes
        if VSAI:
            self.oldarray = self.array
            self.oldarray[x][y]="w"
            self.array = ModelHelper.move(self.array,x,y, board)
        elif VSAI==False:
            if self.player == 0:
                self.oldarray = self.array
                self.oldarray[x][y]="w"
                self.array = ModelHelper.move(self.array,x,y, board)
            else:
                self.oldarray = self.array
                self.oldarray[x][y]="b"
                self.array = ModelHelper.move(self.array,x,y, board)
        Sounds.play_move(mixer)
        self.player = 1-self.player
        self.check_win(screen)
        self.pass_test(screen, depth, board, mixer)
        self.update(screen, depth, VSAI, board, mixer)	

    def draw_score_board(self, screen):
        global moves
        screen.delete("score")

        player1_score = 0
        player2_score = 0
        for x in range(8):
            for y in range(8):
                if self.array[x][y]=="w":
                    player1_score+=1
                elif self.array[x][y]=="b":
                    player2_score+=1

        if self.player==0:
            player_colour = "white"
            second_player = "black"
        else:
            player_colour = "white"
            second_player = "black"

        screen.create_oval(5,540,25,560,fill=player_colour,outline=player_colour)
        screen.create_oval(380,540,400,560,fill=second_player,outline=second_player)

        screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=player1_score)
        screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=player2_score)

        moves = player1_score+player2_score
    def check_win(self, screen):
        player1_score = 0
        player2_score = 0
        for x in range(8):
                for y in range(8):
                    if self.array[x][y]=="w":
                        player1_score+=1
                    elif self.array[x][y]=="b":
                        player2_score+=1
        if(player1_score+player2_score==64):
            if player1_score>player2_score:
                screen.create_text(250,550,anchor="c",font=("Consolas",15), text="White has won!", fill="white")
                return
            elif player2_score>player1_score:
                screen.create_text(250,550,anchor="c",font=("Consolas",15), text="Black has won!", fill="black")
            else:
                screen.create_text(250,550,anchor="c",font=("Consolas",15), text="Draw!", fill="red")
    def pass_test(self, screen, depth, board, mixer):
        mustPass = True
        for x in range(8):
            for y in range(8):
                if ModelHelper.check_move(self.array,self.player,x,y):
                    mustPass=False
        if mustPass:
            self.player = 1-self.player
            if self.passed==True:
                self.won = True
            else:
                self.passed = True
            self.update(screen, depth, VSAI, board, mixer)
        else:
            self.passed = False

    def easy_move(self):
        choices = []
        for x in range(8):
            for y in range(8):
                if ModelHelper.check_move(self.array,self.player,x,y):
                    choices.append([x,y])
        easy_choice = choice(choices)
        self.arrayMove(easy_choice[0],easy_choice[1])

    def medium_move(self, board):
        boards = []
        choices = []
        for x in range(8):
            for y in range(8):
                if ModelHelper.check_move(self.array,self.player,x,y):
                    test = ModelHelper.move(self.array,x,y, board)
                    boards.append(test)
                    choices.append([x,y])

        bestScore = -float("inf")
        bestIndex = 0
        for i in range(len(boards)):
            score = ModelHelper.easy_score(boards[i],self.player)
            if score>bestScore:
                bestIndex=i
                bestScore = score
        self.arrayMove(choices[bestIndex][0],choices[bestIndex][1])

    def hard_move(self, board):
        boards = []
        choices = []
        for x in range(8):
            for y in range(8):
                if ModelHelper.check_move(self.array,self.player,x,y):
                    test = ModelHelper.move(self.array,x,y, board)
                    boards.append(test)
                    choices.append([x,y])

        bestScore = -float("inf")
        bestIndex = 0
        for i in range(len(boards)):
            score= ModelHelper.medium_score(boards[i],self.player)
            if score>bestScore:
                bestIndex=i
                bestScore = score
        self.arrayMove(choices[bestIndex][0],choices[bestIndex][1])

    def minimax(self, node, depth, maximizing, board):
        global nodes
        nodes += 1
        boards = []
        choices = []

        for x in range(8):
            for y in range(8):
                if ModelHelper.check_move(self.array,self.player,x,y):
                    test = ModelHelper.move(node,x,y, board)
                    boards.append(test)
                    choices.append([x,y])

        if depth==0 or len(choices)==0:
            return ([ModelHelper.hard_score(node,1-maximizing),node])

        if maximizing:
            bestValue = -float("inf")
            bestBoard = []
            for board in boards:
                val = self.minimax(board,depth-1,0)[0]
                if val>bestValue:
                    bestValue = val
                    bestBoard = board
            return ([bestValue,bestBoard])

        else:
            bestValue = float("inf")
            bestBoard = []
            for board in boards:
                val = self.minimax(board,depth-1,1)[0]
                if val<bestValue:
                    bestValue = val
                    bestBoard = board
            return ([bestValue,bestBoard])

    def alphaBeta(self,node,depth,alpha,beta,maximizing, boardf):
        global nodes
        nodes += 1
        boards = []
        choices = []

        for x in range(8):
            for y in range(8):
                if ModelHelper.check_move(self.array,self.player,x,y):
                    test = ModelHelper.move(node,x,y,boardf)
                    boards.append(test)
                    choices.append([x,y])

        if depth==0 or len(choices)==0:
            return ([ModelHelper.final_score(array = node,player = maximizing),node])

        if maximizing:
            v = -float("inf")
            bestBoard = []
            bestChoice = []
            for board in boards:
                boardValue = self.alphaBeta(board,depth-1,alpha,beta,0, boardf)[0]
                if boardValue>v:
                    v = boardValue
                    bestBoard = board
                    bestChoice = choices[boards.index(board)]
                alpha = max(alpha,v)
                if beta <= alpha:
                    break
            return([v,bestBoard,bestChoice])
        else:
            v = float("inf")
            bestBoard = []
            bestChoice = []
            for board in boards:
                boardValue = self.alphaBeta(board,depth-1,alpha,beta,1, boardf)[0]
                if boardValue<v:
                    v = boardValue
                    bestBoard = board
                    bestChoice = choices[boards.index(board)]
                beta = min(beta,v)
                if beta<=alpha:
                    break
            return([v,bestBoard,bestChoice])