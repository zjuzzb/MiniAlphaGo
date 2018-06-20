class State():
    def __init__(self):
        # black first, -1 for black, 1 for white
        self.player = -1
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.neighbor = [
            (1, 0),     # right
            (0, 1),     # up
            (-1, 0),    # left
            (0, -1),    # down
        ]
        self.itermap = [[0 for _ in range(9)] for _ in range(9)]

# Create a deep clone of this game state.
    def clone(self):
        st = State()
        st.player = self.player
        st.board = [self.board[i][:] for i in range(9)]
        return st

    def get_moves(self):
        # res = (x, y)
        res = []

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    if self.is_koish(i, j, self.player):
                        res.append((i,j))
        return res

    def is_koish(self, x, y, color, board = None):
        if not board:
            board = self.board
        self.itermap = [[0 for _ in range(9)] for _ in range(9)]
        return self.is_koish_iter(x, y, color, board)

    def is_koish_iter(self, x, y, color, board):
        res = False
        self.itermap[x][y] = 1
        for (dx, dy) in self.neighbor:
            if self.in_bound(x+dx,y+dy):
                if board[x+dx][y+dy] == 0 and self.itermap[x+dx][y+dy] == 0:
                    return True
                elif board[x+dx][y+dy] == color and self.itermap[x+dx][y+dy] == 0:
                    res = self.is_koish_iter(x+dx,y+dy,color, board) or res
        return res

    def pick(self,x ,y, color):
        temp = [self.board[i][:] for i in range(9)]
        temp[x][y] = color
        res = []

        for (dx, dy) in self.neighbor:
            if self.in_bound(x+dx,y+dy):
                if not self.is_koish(x+dx,y+dy,-color,temp) and temp[x+dx][y+dy] == -color:
                    for i in range(9):
                        for j in range(9):
                            if self.itermap[i][j] == 1:
                                temp[i][j] = 0
                                res.append((i,j))
        if self.is_koish(x,y,color,temp) and res:
            self.board = [temp[i][:] for i in range(9)]
            self.board[x][y] = 0
        else:
            res = []
        return res


    @staticmethod
    def in_bound(x, y):
        if x > 8 or x < 0 or y > 8 or y < 0:
            return False
        else:
            return True

    def count(self):
        white = 0
        black = 0

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 1:
                    white += 1
                elif self.board[i][j] == -1:
                    black += 1
        return [white, black]