import random
#creating table for game results using MYSQL
import mysql.connector as sqltor
mycon=sqltor.connect(host="localhost",user="root",password="pingu", database="sadhana")
cursor=mycon.cursor()
cursor.execute("use sadhana;")
cursor.execute("drop table  IF EXISTS score_board;")
cursor.execute("CREATE table score_board(round int, winner varchar(50), piece_chosen varchar(50),total_moves int);")

# Constants to represent the players and empty spaces
PLAYER = 'X'
AI = 'O'
EMPTY = ' '
board = [" " for x in range(9)]

#gathering players infomations
print("WELCOME TO GAME CENTER")
flag=True
while flag:
    number=int(input("how many players?"))
    if number==2:
        xplayer_name=input("Player X: ")
        oplayer_name=input("Player O: ")
        flag=False
    elif number==1:
        xplayer_name=input("Player X: ")
        print(xplayer_name.upper(),"VS COMPUTER")
        flag=False
    else:
        print("Only 1 or 2 player(s) can play")
        
    
#code for the game using python
print()
print("lets play TIC TAC TOE!")
print("YOU GOT 5 ROUNDS! LETS GO!!")
#creating a board for the game
print()

def showboard():
    row1 = "| {} | {} | {} |".format(board[0], board[1], board[2])
    row2 = "| {} | {} | {} |".format(board[3], board[4], board[5])
    row3 = "| {} | {} | {} |".format(board[6], board[7], board[8])
    print()
    print(row1)
    print(row2)
    print(row3)
    print()


#clearing after a round
def clearboard():
    global board
    board = [" " for x in range(9)]


#if opponent is computer
def possibilities(board):
    l=[]
    for i in range(len(board)):
        if board[i]==" ":
            l.append(i)
    return l
           
#players move in board
def players_move(piece):
    flag1=True
    while flag1:
        try:
            if piece == "X":
                name="X"
                print("Your turn player",name)
                choice = int(input("Enter your move (1-9): ").strip())
                if board[choice - 1] == " ":
                    board[choice - 1] = piece
                    flag1=False
                else:
                    print()
                    print("That space is already taken!, Try again..")      
            elif piece == "O":
                name="O"
                print("Your turn player",name)
                choice = int(input("Enter your move (1-9): ").strip())
                if board[choice - 1] == " ":
                    board[choice - 1] = piece
                    flag1=False
                else:
                    print()
                    print("That space is already taken!, Try again..")                
            
            elif piece=="AI":
                print("AI's turn")
                minimax(board, 0, True)
                row= ai_move(board)
                board[row] = AI
                flag1=False
                      
        except IndexError:
            print("Enter your choice within range..")

#checking the contions to win the game
def victory(piece):
    if (board[0] == piece and board[1] == piece and board[2] == piece) or \
       (board[3] == piece and board[4] == piece and board[5] == piece) or \
       (board[6] == piece and board[7] == piece and board[8] == piece) or \
       (board[0] == piece and board[3] == piece and board[6] == piece) or \
       (board[1] == piece and board[4] == piece and board[7] == piece) or \
       (board[2] == piece and board[5] == piece and board[8] == piece) or \
       (board[0] == piece and board[4] == piece and board[8] == piece) or \
       (board[2] == piece and board[4] == piece and board[6] == piece):
        return True
    else:
        return False


#checking whether the match is draw
def draw():
    if " " not in board:
        return True
    else:
        return False

    
#finding overall winner
def overallwin():
    cursor.execute("select * from score_board;")
    data=cursor.fetchall()
    cntx,cnto=0,0
    for i in data:
        if i[2]=="X":
            cntx+=1
        else:
            cnto+=1
    if cntx>cnto:
         print("OVERALL WINNER IS",xplayer_name.upper())
    else:
        print("OVERALL WINNER IS",oplayer_name.upper())
        
def total_moves(board):
    cnt=0
    for i in board:
        if i!=" ":
            cnt+=1
    return cnt       

# Minimax Algorithm
def minimax(board, depth, is_maximizing):
    # If AI wins, return a positive score
    if victory(AI):
        return 10 - depth
    # If Player wins, return a negative score
    if victory(PLAYER):
        return depth - 10
    # If board is full, it's a tie
    if draw():
        return 0
    
    if is_maximizing:
        max_eval = float('-inf')
        for row in range(9):
                if board[row] == EMPTY:
                    board[row] = AI
                    eval = minimax(board, depth + 1, False)
                    board[row]= EMPTY
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(9):
                if board[row] == EMPTY:
                    board[row] = PLAYER
                    eval = minimax(board, depth + 1, True)
                    board[row]= EMPTY
                    min_eval = min(min_eval, eval)
        return min_eval

# AI Move (using minimax to find the best move)
def ai_move(board):
    best_move = None
    best_value = float('-inf')
    
    for row in range(9):
        
            if board[row]== EMPTY:
                board[row]= AI
                move_value = minimax(board, 0, False)
                board[row] = EMPTY
                if move_value > best_value:
                    best_value = move_value
                    best_move = row
    
    return best_move




#execution of game
for i in range(1,6):
    print("ROUND",i,"!")
    while True:
            showboard()
            players_move("X")
            showboard()
            if victory("X"):
                print("X wins!!")
                print("THE WINNER OF ROUND",i,"IS",xplayer_name.upper(),"!")
                winner=xplayer_name
                win_piece="X"
                moves=total_moves(board)
                query1="INSERT INTO score_board values({},'{}','{}',{})".format(i,winner,win_piece,moves)
                cursor.execute(query1)
                mycon.commit()
                break
            elif draw():
                print("It's a draw!")
                winner="draw"
                win_piece="none"
                moves=total_moves(board)
                query1="INSERT INTO score_board values({},'{}','{}',{})".format(i,winner,win_piece,moves)
                break
            if number==1:
                players_move("AI")
                oplayer_name="AI"
            else:
                players_move("O")
            if victory("O"):
                showboard()
                print("O wins!!")
                print("THE WINNER OF ROUND",i,"IS",oplayer_name.upper(),"!")
                winner=oplayer_name
                win_piece="O"
                moves=total_moves(board)
                query1="INSERT INTO score_board values({},'{}','{}',{})".format(i,winner,win_piece,moves)
                cursor.execute(query1)
                mycon.commit()
                break
                
            elif draw():
                print("It's a draw!")
                win_piece="draw"
                winner="none"
                moves=total_moves(board)
                query1="INSERT INTO score_board values({},'{}','{}',{})".format(i,winner,win_piece,moves)
                cursor.execute(query1)
                mycon.commit()
                break       
    clearboard()  
print()
overallwin()
print("GAME OVER!")
board = [" " for x in range(9)]
