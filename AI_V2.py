class AI:
    def promote_pawn(self, board):
        rand = random.randint(1, 4) # random integer
        pieces = ['q', 'r', 'b', 'k'] # list of available promotions
        
        return pieces[rand] # return a random promotion piece



    def assess_moves(self):
        pass


    
    def make_move(self, input_board, proficiency, colour):
        self.assess_moves()


    
    def __init__(self, main):
        self.board = []
        self.main = main


import copy, random, numpy
