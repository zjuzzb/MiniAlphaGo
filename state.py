class State():
    def __init__(self):
        # black first, -1 for black, 1 for white
        self.player = -1
        self.board = [[0 for _ in range(9)] for _ in range(9)]

# Create a deep clone of this game state.
    def clone(self):
        st = State()
        st.player = self.player
        st.board = [self.board[i][:] for i in range(8)]
        return st

    def get_moves(self):
        # res = (x, y)
        res = []

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    res.append((i,j))
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