from copy import deepcopy
moves = 0
class ModelHelper:
    def move(passedArray,x,y, board):
        array = deepcopy(passedArray)
        if board.player==0:
            colour = "w"
        else:
            colour="b"
        array[x][y]=colour
        
        neighbours = []
        for i in range(max(0,x-1),min(x+2,8)):
            for j in range(max(0,y-1),min(y+2,8)):
                if array[i][j]!=None:
                    neighbours.append([i,j])
        
        convert = []
        for neighbour in neighbours:
            neighX = neighbour[0]
            neighY = neighbour[1]
            if array[neighX][neighY]!=colour:
                path = []
                
                deltaX = neighX-x
                deltaY = neighY-y

                tempX = neighX
                tempY = neighY

                while 0<=tempX<=7 and 0<=tempY<=7:
                    path.append([tempX,tempY])
                    value = array[tempX][tempY]
                    if value==None:
                        break
                    if value==colour:
                        for node in path:
                            convert.append(node)
                        break
                    tempX+=deltaX
                    tempY+=deltaY
                    
        for node in convert:
            array[node[0]][node[1]]=colour

        return array

    def grid_background(screen, outline=False):
        if outline:
            screen.create_rectangle(50,50,450,450,outline="#111")

        for i in range(7):
            lineShift = 50+50*(i+1)

            screen.create_line(50,lineShift,450,lineShift,fill="#111")

            screen.create_line(lineShift,50,lineShift,450,fill="#111")

        screen.update()

    def easy_score(array,player):
        score = 0
        if player==1:
            colour="b"
            opponent="w"
        else:
            colour = "w"
            opponent = "b"
        for x in range(8):
            for y in range(8):
                if array[x][y]==colour:
                    score+=1
                elif array[x][y]==opponent:
                    score-=1
        return score

    def medium_score(array,player):
        score = 0
        if player==1:
            colour="b"
            opponent="w"
        else:
            colour = "w"
            opponent = "b"
        for x in range(8):
            for y in range(8):
                add = 1
                if (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
                    add=3
                elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
                    add = 5
                if array[x][y]==colour:
                    score+=add
                elif array[x][y]==opponent:
                    score-=add
        return score

    def hard_score(array,player):
        score = 0
        cornerVal = 25
        adjacentVal = 5
        sideVal = 5
        if player==1:
            colour="b"
            opponent="w"
        else:
            colour = "w"
            opponent = "b"
        for x in range(8):
            for y in range(8):
                add = 1
                
                if (x==0 and y==1) or (x==1 and 0<=y<=1):
                    if array[0][0]==colour:
                        add = sideVal
                    else:
                        add = -adjacentVal


                elif (x==0 and y==6) or (x==1 and 6<=y<=7):
                    if array[7][0]==colour:
                        add = sideVal
                    else:
                        add = -adjacentVal

                elif (x==7 and y==1) or (x==6 and 0<=y<=1):
                    if array[0][7]==colour:
                        add = sideVal
                    else:
                        add = -adjacentVal

                elif (x==7 and y==6) or (x==6 and 6<=y<=7):
                    if array[7][7]==colour:
                        add = sideVal
                    else:
                        add = -adjacentVal


                elif (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
                    add=sideVal
                elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
                    add = cornerVal
                if array[x][y]==colour:
                    score+=add
                elif array[x][y]==opponent:
                    score-=add
        return score

    def final_score(array, player):
        global moves
        if moves<=8:
            numMoves = 0
            for x in range(8):
                for y in range(8):
                    if ModelHelper.check_move(array,player,x,y):
                        numMoves += 1
            return numMoves+ModelHelper.hard_score(array,player)
        elif moves<=52:
            return ModelHelper.hard_score(array,player)
        elif moves<=58:
            return ModelHelper.medium_score(array,player)
        else:
            return ModelHelper.easy_score(array,player)

    def check_move(array,player,x,y):
        if player==0:
            colour="w"
        else:
            colour="b"
            
        if array[x][y]!=None:
            return False

        else:
            neighbour = False
            neighbours = []
            for i in range(max(0,x-1),min(x+2,8)):
                for j in range(max(0,y-1),min(y+2,8)):
                    if array[i][j]!=None:
                        neighbour=True
                        neighbours.append([i,j])
            if not neighbour:
                return False
            else:
                valid = False
                for neighbour in neighbours:

                    neighX = neighbour[0]
                    neighY = neighbour[1]
                    
                    if array[neighX][neighY]==colour:
                        continue
                    else:
                        deltaX = neighX-x
                        deltaY = neighY-y
                        tempX = neighX
                        tempY = neighY

                        while 0<=tempX<=7 and 0<=tempY<=7:
                            if array[tempX][tempY]==None:
                                break
                            if array[tempX][tempY]==colour:
                                valid=True
                                break
                            tempX+=deltaX
                            tempY+=deltaY
                return valid