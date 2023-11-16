'''Each of the following classes defines a specfic piece
type. Each comes with built in values that are defined
upon creation and correspond to relvant piece info. The
classes define the board pieces as objects, making them
easier to access and draw information from. They also
come with an in-built 'get_available_moves' function that
returns all legal moves available to the piece (not
considering check restrictions).
'''



class Empty_Square:
    def destroy(self):
        pass


    
    def __init__(self):
        self.value = None
        self.pos = [None, None]
        self.colour = None
        self.available_moves = None
        self.name = None
        self.code = '--'
        self.has_moved = None



class Pawn:
    def get_available_moves(self, board, ignore_own_pieces):
        row, col = self.pos
        self.available_moves = []
        moves = []


        #different colours move in different directions
        if self.colour == 'white':
            if row - 1 >= 0:
                if col - 1 >= 0:
                    if board[row - 1][col - 1].name != None:
                        moves.append([row - 1, col - 1])


                if col + 1 < 8:
                    if board[row - 1][col + 1].name != None:
                        moves.append([row - 1, col + 1])


                if row - 1 >= 0:
                    if board[row - 1][col].name == None:
                        moves.append([row - 1, col])

                        if row - 2 >= 0 and not self.has_moved:
                            if board[row - 2][col].name == None:
                                moves.append([row - 2, col])

        else:
            if row + 1 < 8:
                if col - 1 >= 0 and board[row + 1][col - 1].name != None:
                    moves.append([row + 1, col - 1])


                if col + 1 < 8 and board[row + 1][col + 1].name != None:
                    moves.append([row + 1, col + 1])


                if row + 1 < 8:
                    if board[row + 1][col].name == None:
                        moves.append([row + 1, col])

                        if row + 2 < 8:
                            if board[row + 2][col].name == None and not self.has_moved:
                                moves.append([row + 2, col])

            #board is oriented from whites perspective. Black pawns move down rows


        if not ignore_own_pieces:
            for move in moves:
                rw, cl = move

                if board[rw][cl].colour != self.colour:
                    self.available_moves.append(move)

        else:
            self.available_moves = moves


        return self.available_moves


    
    def __init__(self, colour):
        self.value = 1
        self.pos = [None, None]
        self.colour = colour
        self.available_moves = []
        self.name = 'pawn'
        self.code = colour[0] + 'P'
        self.has_moved = False



class Knight:
    def get_available_moves(self, board, ignore_own_pieces):
        row, col = self.pos
        self.available_moves = []
        
        moves = [[row - 2, col - 1], [row - 2, col + 1],
                 [row + 2, col - 1], [row + 2, col + 1],
                 [row - 1, col - 2], [row + 1, col - 2],
                 [row - 1, col + 2], [row + 1, col + 2]]


        if not ignore_own_pieces:
            for move in moves:
                rw, cl = move
                
                if rw < 0 or rw >= 8 or cl < 0 or cl >= 8:
                    continue
                else:
                    if board[rw][cl].colour != self.colour:
                        self.available_moves.append(move)

        else:
            for move in moves:
                rw, cl = move
                        
                if rw < 0 or rw >= 8 or cl < 0 or cl >= 8:
                    continue
                else:
                    self.available_moves.append(move)


        return self.available_moves
        

    
    def __init__(self, colour):
        self.value = 1
        self.pos = [None, None]
        self.colour = colour
        self.available_moves = []
        self.name = 'knight'
        self.code = colour[0] + 'N'
        self.has_moved = False


    
class Bishop:
    def get_available_moves(self, board, ignore_own_pieces):
        row, col = self.pos
        self.available_moves = []
        moves = []

        for i in range(1, 8):          #upper left diagonal
            rw, cl = [row - i, col - i]

            if rw < 0 or cl < 0:
                break
            
            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break

            
        for i in range(1, 8):           #lower right diagonal
            rw, cl = [row + i, col + i]

            if rw >= 8 or cl >= 8:
                break

            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break

            
        for i in range(1, 8):               #lower left diagonal
            rw, cl = [row + i, col - i]

            if rw >= 8 or cl < 0:
                break

            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break


        for i in range(1, 8):               #upper right diagonal
            rw, cl = [row - i, col + i]

            if rw < 0 or cl >= 8:
                break
            
            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break


        if not ignore_own_pieces:
            for move in moves:
                rw, cl = move
                
                if board[rw][cl].colour != self.colour:
                    self.available_moves.append(move)

        else:
            for move in moves:
                if rw < 0 or rw >= 8 or cl < 0 or cl >= 8:
                    continue
                else:
                    self.available_moves.append(move)


        return self.available_moves


    
    def __init__(self, colour):
        self.value = 1
        self.pos = [None, None]
        self.colour = colour
        self.available_moves = []
        self.name = 'bishop'
        self.code = colour[0] + 'B'
        self.has_moved = False


    
class Rook:
    def get_available_moves(self, board, ignore_own_pieces):
        row, col = self.pos
        self.available_moves = []
        moves = []


        for i in range(1, col + 1):             #row to the left of piece
            rw, cl = [row, col - i]

            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break


        for i in range(col + 1, 8):
            rw, cl = [row, i]
            
            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break


        for i in range(1, row + 1):
            rw, cl = [row - i, col]
            
            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break
        

        for i in range(row + 1, 8):
            rw, cl = [i, col]
            
            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break


        if not ignore_own_pieces:
            for move in moves:
                rw, cl = move
                
                if board[rw][cl].colour != self.colour:
                    self.available_moves.append(move)

        else:
            for move in moves:
                if rw < 0 or rw >= 8 or cl < 0 or cl >= 8:
                    continue
                else:
                    self.available_moves.append(move)
            

        return self.available_moves


    
    def __init__(self, colour):
        self.value = 1
        self.pos = [None, None]
        self.colour = colour
        self.available_moves = []
        self.name = 'rook'
        self.code = colour[0] + 'R'
        self.has_moved = False


    
class Queen:
    def get_available_moves(self, board, ignore_own_pieces):
        row, col = self.pos
        moves = []
        self.available_moves = []


        #straights
        for i in range(1, col + 1):             #row to the left of piece
            moves.append([row, col - i])
            
            if board[row][col - i].name != None:
                break


        for i in range(col + 1, 8):             #right row
            moves.append([row, i])
            
            if board[row][i].name != None:
                break


        for i in range(1, row + 1):             #upper column
            moves.append([row - i, col])
            
            if board[row - i][col].name != None:
                break
        

        for i in range(row + 1, 8):             #lower column
            moves.append([i, col])
            
            if board[i][col].name != None:
                break


        #diagonals
        for i in range(1, 8):          #upper left diagonal
            rw, cl = [row - i, col - i]

            if rw < 0 or cl < 0:
                break
            
            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break

            
        for i in range(1, 8):           #lower right diagonal
            rw, cl = [row + i, col + i]

            if rw >= 8 or cl >= 8:
                break
            
            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break

            
        for i in range(1, 8):               #lower left diagonal
            rw, cl = [row + i, col - i]

            if rw >= 8 or cl < 0:
                break

            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break


        for i in range(1, 8):               #upper right diagonal
            rw, cl = [row - i, col + i]

            if rw < 0 or cl >= 8:
                break
            
            moves.append([rw, cl])
            
            if board[rw][cl].name != None:
                break


        if not ignore_own_pieces:
            for move in moves:
                rw, cl = move

                if board[rw][cl].colour != self.colour:
                    self.available_moves.append(move)

        else:
            '''for move in moves:
                if rw < 0 or rw >= 8 or cl < 0 or cl >= 8:
                    continue
                else:'''
            self.available_moves = moves


        return self.available_moves

    
    def __init__(self, colour):
        self.value = 1
        self.pos = [None, None]
        self.colour = colour
        self.available_moves = []
        self.name = 'queen'
        self.code = colour[0] + 'Q'
        self.has_moved = False



class King:
    def get_available_moves(self, board, ignore_own_pieces):
        row, col = self.pos
        
        #the eight squares surrounding the king
        moves = [[row - 1, col - 1], [row - 1, col], [row - 1, col + 1], [row, col - 1],
                 [row, col + 1], [row + 1, col - 1], [row + 1, col], [row + 1, col + 1]]

        self.available_moves = []


        if not ignore_own_pieces:
            for move in moves:
                rw, cl = move
                
                if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                    if board[rw][cl].colour != self.colour:
                        self.available_moves.append(move)


            #check for castling
            if not self.has_moved:
                if board[row][col + 3].code == self.code[0] + 'R' and not board[row][col + 3].has_moved:
                    if board[row][col + 1].name == None and board[row][col + 2].name == None:
                        self.available_moves.append([[row, col + 2], [row, col + 3], [row, col + 1]])
                        
        else:
            for move in moves:
                rw, cl = move
                
                if rw < 0 or rw >= 8 or cl < 0 or cl >= 8:
                    continue
                else:
                    self.available_moves.append(move)
                    

        return self.available_moves



    def destroy(self):
        del self


    
    def __init__(self, colour):
        self.value = 1
        self.pos = [None, None]
        self.colour = colour
        self.available_moves = []
        self.name = 'king'
        self.code = colour[0] + 'K'
        self.has_moved = False
