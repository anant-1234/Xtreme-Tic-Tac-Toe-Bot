import copy
import time
# f = 0
class Team16:
    defence = 1
    subs = []
    def __init__(self):
        pass

    def mupdate(self, board, old_move, new_move, ply):
        #updating the game board and small_board status as per the move that has been passed in the arguements
        # if(self.check_valid_move(old_move, new_move)) == False:
        #     return 'UNSUCCESSFUL', False
        board.big_boards_status[new_move[0]][new_move[1]][new_move[2]] = ply

        x = new_move[1]/3
        y = new_move[2]/3
        k = new_move[0]
        fl = 0

        #checking if a small_board has been won or drawn or not after the current move
        bs = board.big_boards_status[k]
        for i in range(3):
            #checking for horizontal pattern(i'th row)
            if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == ply):
                board.small_boards_status[k][x][y] = ply
                return 'SUCCESSFUL', True
            #checking for vertical pattern(i'th column)
            if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == ply):
                board.small_boards_status[k][x][y] = ply
                return 'SUCCESSFUL', True
        #checking for diagonal patterns
        #diagonal 1
        if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == ply):
            board.small_boards_status[k][x][y] = ply
            return 'SUCCESSFUL', True
        #diagonal 2
        if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == ply):
            board.small_boards_status[k][x][y] = ply
            return 'SUCCESSFUL', True
        #checking if a small_board has any more cells left or has it been drawn
        for i in range(3):
            for j in range(3):
                if bs[3*x+i][3*y+j] =='-':
                    return 'SUCCESSFUL', False
        board.small_boards_status[k][x][y] = 'd'
        return 'SUCCESSFUL', False

    def minimax(self,board,old_move,flag,depth,p_win, poss_boards,alpha,beta):
        # global f
        # f+=1
        if flag == 'o':
           best = [-1,-1,-1, -10000000000000000]
        else:
           best = [-1,-1,-1, +10000000000000000]

        if depth == 0:      
            value = self.calculate_heuristic(board,flag,poss_boards, p_win);
            return [-2, -1 , -1, value];

        cells = board.find_valid_move_cells(old_move)
        # if len(cells) == 0:
        #     # return [old_move[0], old_move[1], old_move[2],0]
        #     # print old_move
        #     print(depth)
        #     # print "chutiye"
        #     # ch = raw_input()
        #     # time.sleep(10)
        for cell in cells:
            x,y,z = cell[0],cell[1],cell[2]
            poss_boards.append(cell)

            self.mupdate(board,old_move, [x,y,z], flag)

            if(self.mywin([x,y,z],board,flag) == 1 and p_win == 0):
                bmove = self.minimax(board,[x,y,z],flag,depth-1,1,poss_boards,alpha,beta)

            else:
                if flag == 'x':
                    bmove = self.minimax(board,[x,y,z],'o',depth-1,0,poss_boards,alpha,beta)
                if flag == 'o':
                    bmove = self.minimax(board,[x,y,z],'x',depth-1,0,poss_boards,alpha,beta)

                    
            board.big_boards_status[x][y][z] = '-'
            board.small_boards_status[x][y/3][z/3] = '-'
            if(y%3==1 and z%3==1):
                if flag=='o':
                    bmove[3]+=1;
                elif flag=='x':
                    bmove[3]-=1;


            poss_boards.pop()
            bmove[0],bmove[1],bmove[2] = x,y,z;
            # if x == -1:
            #     print bmove
            #     print "noo"
            #     time.sleep(10)
            if flag == 'o':
                if bmove[3] >= best[3]:
                    best = bmove  # max value        
                alpha = max(alpha,best[3])       
            else:
                if bmove[3] < best[3]:
                    best = bmove  # min value
                beta = min(beta,best[3])
        # print "arnav"
        # print best
        # time.sleep(10);
            if alpha > beta:
                break
        return best

    def mywin(self,mymove,board_state, ch):
      
        x = mymove[1]/3
        y = mymove[2]/3
        z = mymove[0]
        
        haswon = 0;
        
        bs = board_state.big_boards_status[z]
        for i in range(3):
            #checking for horizontal pattern(i'th row)
            if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == ch):
                haswon = 1
            #checking for vertical pattern(i'th column)
            if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == ch):
                haswon = 1
            
            if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == ch):
                haswon = 1
            
            if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == ch):
                haswon = 1
            
        return haswon



    def calculate_heuristic(self,bs,ch,poss_boards,p_win):
        if ch == 'x':
            op_ch = 'o'
        if ch == 'o':
            op_ch = 'x'

        bs2 = bs
        scoremf = 0
        factor = 1500  # Winning triplets in Small Boards
        factor6 = 1200 # Blocking on small boards

        factor2 = 2500 # Winning Triplets in Big Board(Entire Game)
        factor5 = 1700 # Blocking on big boards
        factor7 = 700   # oo* on smaller boards
        factor8 = 900   # oo* on bigger boards
        factor9 = 0
        ssmall_boards_status = copy.deepcopy(bs2.small_boards_status)
        poss_boards.reverse()
        for mv in poss_boards:
            x = mv[1]/3
            y = mv[2]/3
            z = mv[0]
            factor *= 6 
            factor2 *= 9
            factor5 *= 7
            factor6 *= 5
            factor7 *= 4
            factor8 *= 6
            factor9 *= 2

            bs = copy.deepcopy(bs2.big_boards_status[z])
            for i in range(3):
                    #checking for horizontal pattern(i'th row)
                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == 'o'):
                    ssmall_boards_status[z][x][y] = 'o'
                    if x%3 == 1 and y%3 == 1:
                        scoremf += factor9
                    scoremf += factor
                    scoremf += self.count(ssmall_boards_status[z], x, y, 'x', 'x') * factor5
                    scoremf += self.count(ssmall_boards_status[z], x, y, 'o', '-') * factor8 
                    scoremf += self.count(ssmall_boards_status[z], x, y, '-', 'o') * factor8 

                #checking for vertical pattern(i'th column)
                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == 'o'):
                    ssmall_boards_status[z][x][y] = 'o'
                    if x%3 == 1 and y%3 == 1:
                        scoremf += factor9
                    scoremf += factor
                    scoremf += self.count(ssmall_boards_status[z], x, y, 'x', 'x') * factor5
                    scoremf += self.count(ssmall_boards_status[z], x, y, 'o', '-') * factor8 
                    scoremf += self.count(ssmall_boards_status[z], x, y, '-', 'o') * factor8 

            

                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == 'x'):
                    scoremf-=factor
                    ssmall_boards_status[z][x][y] = 'x'
                    if x%3 == 1 and y%3 == 1:
                        scoremf -= factor9
                    scoremf -= self.count(ssmall_boards_status[z], x, y, 'o', 'o') * factor5
                    scoremf -= self.count(ssmall_boards_status[z], x, y, '-', 'x') * factor8 
                    scoremf -= self.count(ssmall_boards_status[z], x, y, 'x', '-') * factor8 


                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == 'x'):
                    scoremf-=factor
                    ssmall_boards_status[z][x][y] = 'x'
                    if x%3 == 1 and y%3 == 1:
                        scoremf -= factor9
                    scoremf -= self.count(ssmall_boards_status[z], x, y, 'o' ,'o') * factor5 
                    scoremf -= self.count(ssmall_boards_status[z], x, y, 'x', '-') * factor8 
                    scoremf -= self.count(ssmall_boards_status[z], x, y, '-', 'x') * factor8 


                
            # Diagonals of Triplets
            
            if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == 'o'):
                ssmall_boards_status[z][x][y] = 'o'
                if x%3 == 1 and y%3 == 1:
                    scoremf += factor9
                scoremf += factor
                scoremf += self.count(ssmall_boards_status[z], x, y, 'x', 'x') * factor5
                scoremf += self.count(ssmall_boards_status[z], x, y, 'o', '-') * factor8 
                scoremf += self.count(ssmall_boards_status[z], x, y, '-', 'o') * factor8 



            if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == 'o'):
                ssmall_boards_status[z][x][y] = 'o'
                if x%3 == 1 and y%3 == 1:
                    scoremf += factor9
                scoremf += factor
                scoremf += self.count(ssmall_boards_status[z], x, y, 'x', 'x') * factor5 
                scoremf += self.count(ssmall_boards_status[z], x, y, 'o', '-') * factor8 
                scoremf += self.count(ssmall_boards_status[z], x, y, '-', 'o') * factor8 



            if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == 'x'):
                ssmall_boards_status[z][x][y] = 'x'
                if x%3 == 1 and y%3 == 1:
                    scoremf -= factor9
                scoremf -= factor
                scoremf -= self.count(ssmall_boards_status[z], x, y, 'o', 'o') * factor5
                scoremf -= self.count(ssmall_boards_status[z], x, y, '-', 'x') * factor8 
                scoremf -= self.count(ssmall_boards_status[z], x, y, 'x', '-') * factor8 


            if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == 'x'):
                scoremf -= factor
                ssmall_boards_status[z][x][y] = 'x'
                if x%3 == 1 and y%3 == 1:
                    scoremf -= factor9
                scoremf -= self.count(ssmall_boards_status[z], x, y, 'o', 'o') * factor5
                scoremf -= self.count(ssmall_boards_status[z], x, y, '-', 'x') * factor8 
                scoremf -= self.count(ssmall_boards_status[z], x, y, 'x', '-') * factor8 



            
            if bs[mv[1]][mv[2]] == 'o':
                val = self.count_small(bs, mv[1], mv[2], 'x', 'x') * factor6
                val2 = self.count_small(bs, mv[1], mv[2], 'o' , '-') * factor7
                val3 = self.count_small(bs, mv[1], mv[2], '-' , 'o') * factor7
                scoremf += val + val2 + val3

            elif bs[mv[1]][mv[2]] == 'x':
                val = self.count_small(bs, mv[1], mv[2], 'o', 'o') * factor6
                val2 = self.count_small(bs, mv[1], mv[2], 'x' , '-') * factor7
                val3 = self.count_small(bs, mv[1], mv[2], '-' , 'x') * factor7
                scoremf -= (val + val2 + val3)

            bs[mv[1]][mv[2]] = '-'

            # Small Boards Region

            bs = ssmall_boards_status[z]
            for i in range(3):
            # Rows and columns triplets 
                if (bs[i][0] == bs[i][1] and bs[i][1] == bs[i][2]):
                    if (bs[i][0] == 'o'):
                        scoremf += factor2
                    elif (bs[i][0] == 'x'):
                        scoremf -= factor2
                if (bs[0][i] == bs[1][i] and bs[2][i] == bs[1][i]):
                    if (bs[0][i] == 'o'):
                        scoremf += factor2
                    elif (bs[0][i] == 'x'):
                        scoremf -= factor2


           



           # Diagonals of triplets

            if bs[0][0] == bs[1][1] and bs[1][1] == bs[2][2]:
                if bs[0][0] == 'x':
                    scoremf -= factor2
                elif bs[0][0] == 'o':
                    scoremf += factor2
            if bs[2][0] == bs[1][1] and bs[1][1] == bs[0][2]:
                if bs[1][1] == 'x':
                    scoremf -= factor2
                elif bs[1][1] == 'o':
                    scoremf += factor2 

            # Diagonals of duets

           


        poss_boards.reverse()
        return scoremf
        
        
    def move(self, board, old_move, flag):
        # if flag == 'x':
        #     Team16.defence = 0

        print 'Enter your move: <format:board row column> (you\'re playing with', flag + ")"    
        # if(flag == 'x')
        global f
        f = 0
        Team16.subs = (board.find_valid_move_cells(old_move))[0]
        mvp = self.minimax(board,old_move,flag,3,0,[],-10000000000000000,1000000000000000)
        if mvp[0] == -1 or mvp[1] == -1 or mvp[2] == -1:
            mvp = Team16.subs
        # print(f)
        print(mvp)
        # time.sleep(7);
        # ch = raw_input();

        return (int(mvp[0]), int(mvp[1]), int(mvp[2]))

    def count(self, bs, x, y, ch, ch2):
        cnt = 0
        if x == 0:
            if y == 0:
                if bs[x][y+1] == ch and bs[x][y+2] == ch2:
                    cnt+=1;
                if bs[x+1][y] == ch and bs[x+2][y] == ch2:
                    cnt+=1
                if bs[x+1][y+1] == ch and bs[x+2][y+2] == ch2:
                    cnt+=1
            if y == 1:
                if bs[x][y-1] == ch and bs[x][y+1] == ch2:
                    cnt+=1
                if bs[x+1][y] == ch and bs[x+2][y] == ch2:
                    cnt+=1
            if y == 2:
                if bs[x+1][y] == ch and bs[x+2][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch2:
                    cnt+=1
                if bs[x+1][y-1] == ch and bs[x+2][y-2] == ch2:
                    cnt+=1
        if x == 1:
            if y == 0:
                if bs[x-1][y] == ch and bs[x+1][y] == ch2:
                    cnt+=1
                if bs[x][y+1] == ch and bs[x][y+2] == ch2:
                    cnt+=1;
            if y == 1:
                if bs[x-1][y] == ch and bs[x+1][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y+1] == ch2:
                    cnt+=1
                if bs[x-1][y+1] == ch and bs[x+1][y-1] == ch2:
                    cnt+=1
                if bs[x+1][y+1] == ch and bs[x-1][y-1] == ch2:
                    cnt+=1
            if y == 2:
                if bs[x-1][y] == ch and bs[x+1][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch2:
                    cnt+=1
        if x == 2:
            if y == 0:
                if bs[x-1][y] == ch and bs[x-2][y] == ch2:
                    cnt+=1
                if bs[x][y+1] == ch and bs[x][y+2] == ch2:
                    cnt+=1
                if bs[x-1][y+1] == ch and bs[x-2][y+2] == ch2:
                    cnt+=1
            if y == 1:
                if bs[x-1][y] == ch and bs[x-2][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y+1] == ch2:
                    cnt+=1
            if y == 2:
                if bs[x-1][y] == ch and bs[x-2][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch2:
                    cnt+=1
                if bs[x-1][y-1] == ch and bs[x-2][y-2] == ch2:
                    cnt+=1
        return cnt

    def count_small(self, bs, x, y, ch, ch2):

        cnt = 0
        if x%3 == 0:
            if y%3 == 0:
                if bs[x][y+1] == ch and bs[x][y+2] == ch2:
                    cnt+=1;
                if bs[x+1][y] == ch and bs[x+2][y] == ch2:
                    cnt+=1
                if bs[x+1][y+1] == ch and bs[x+2][y+2] == ch2:
                    cnt+=1
            if y%3 == 1:
                if bs[x][y-1] == ch and bs[x][y+1] == ch2:
                    cnt+=1
                if bs[x+1][y] == ch and bs[x+2][y] == ch2:
                    cnt+=1
            if y%3 == 2:
                if bs[x+1][y] == ch and bs[x+2][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch2:
                    cnt+=1
                if bs[x+1][y-1] == ch and bs[x+2][y-2] == ch2:
                    cnt+=1
        if x%3 == 1:
            if y%3 == 0:
                if bs[x-1][y] == ch and bs[x+1][y] == ch2:
                    cnt+=1
                if bs[x][y+1] == ch and bs[x][y+2] == ch2:
                    cnt+=1;
            if y%3 == 1:
                if bs[x-1][y] == ch and bs[x+1][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y+1] == ch2:
                    cnt+=1
                if bs[x-1][y+1] == ch and bs[x+1][y-1] == ch2:
                    cnt+=1
                if bs[x+1][y+1] == ch and bs[x-1][y-1] == ch2:
                    cnt+=1
            if y%3 == 2:
                if bs[x-1][y] == ch and bs[x+1][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch2:
                    cnt+=1
        if x%3 == 2:
            if y%3 == 0:
                if bs[x-1][y] == ch and bs[x-2][y] == ch2:
                    cnt+=1
                if bs[x][y+1] == ch and bs[x][y+2] == ch2:
                    cnt+=1
                if bs[x-1][y+1] == ch and bs[x-2][y+2] == ch2:
                    cnt+=1
            if y%3 == 1:
                if bs[x-1][y] == ch and bs[x-2][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y+1] == ch2:
                    cnt+=1
            if y%3 == 2:
                if bs[x-1][y] == ch and bs[x-2][y] == ch2:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch2:
                    cnt+=1
                if bs[x-1][y-1] == ch and bs[x-2][y-2] == ch2:
                    cnt+=1
        if Team16.defence == 0:
            if cnt > 2:
                return cnt-1
            elif cnt == 1:
                return 1
            else:
                return 0    
        else:
            return cnt




