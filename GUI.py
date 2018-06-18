from tkinter import *
from tkinter import messagebox
import threading
import time


class GoModel():
    def __init__(self):
        # black first, -1 for black, 1 for white
        self.player = -1
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        # timing
        self.time_white = 0
        self.time_black = 0
        self.step_time = 0
        # for convenience
        self.prev_selected = (-1, -1)


class Application(Frame):
    def __init__(self, model, master=None):
        # load model
        self.model = model
        # add root frame
        Frame.__init__(self, master, height=500, width=500)
        self.pack()
        # load icons
        self.cross_icon = []
        self.cross_highlighted_icon = []
        self.down_edge_icon = []
        self.down_edge_highlighted_icon = []
        self.ld_corner_icon = []
        self.ld_corner_highlighted_icon = []
        self.left_edge_icon = []
        self.left_edge_highlighted_icon = []
        self.lu_corner_icon = []
        self.lu_corner_highlighted_icon = []
        self.rd_corner_icon = []
        self.rd_corner_highlighted_icon = []
        self.right_edge_icon = []
        self.right_edge_highlighted_icon = []
        self.ru_corner_icon = []
        self.ru_corner_highlighted_icon = []
        self.up_edge_icon = []
        self.up_edge_highlighted_icon = []
        self.load_icons()
        # initialize components
        self.chessButton = [[Button(self, bd=0, height=80, width=80, bg='#EBCEAC', image=self.cross_icon[2]) for _ in range(9)] for _ in range(9)]
        self.time_text_black = StringVar(self, 'Black Total: 00:00  Step: 00:00')
        self.time_text_white = StringVar(self, 'White Total: 00:00  Step: 00:00')
        self.player_text = StringVar(self, 'Current Player: Black')
        # load components
        self.create_widgets()
        # add thread for white timing
        self.t_white = threading.Thread(target=self.update_time_text_white, args=(), name='thread-refresh')
        self.t_white.setDaemon(True)
        self.t_white.start()
        # add thread for black timing
        self.t_black = threading.Thread(target=self.update_time_text_black, args=(), name='thread-refresh')
        self.t_black.setDaemon(True)
        self.t_black.start()

    def on_click(self, x, y):
        if self.model.board[x][y] == 0:
            if self.model.player == -1:
                icon = self.get_icon(x, y, 1, True)
            else:
                icon = self.get_icon(x, y, 0, True)
            # put chess on the board and the model
            self.model.board[x][y] = self.model.player
            self.chessButton[x][y].config(image=icon)
            # clear previous selected icon
            (prev_x, prev_y) = self.model.prev_selected
            if (prev_x, prev_y) != (-1, -1):
                if self.model.player == 1:
                    icon = self.get_icon(prev_x, prev_y, 1, False)
                else:
                    icon = self.get_icon(prev_x, prev_y, 0, False)
                self.chessButton[prev_x][prev_y].config(image=icon)
            # store new selected location
            self.model.prev_selected = (x, y)
            # clear step timing
            self.model.step_time = 0
            # change player
            self.model.player = -self.model.player

    def create_widgets(self):
        self.time_label_white = Label(self, textvariable=self.time_text_white)
        self.time_label_white.grid(row=0, column=0, columnspan=3)
        self.time_label_black = Label(self, textvariable=self.time_text_black)
        self.time_label_black.grid(row=0, column=6, columnspan=3)
        self.player_label = Label(self, textvariable=self.player_text)
        self.player_label.grid(row=0, column=3, columnspan=3)

        for i in range(9):
            for j in range(9):
                self.chessButton[i][j].config(image=self.get_icon(i, j, 2, False))
                self.chessButton[i][j].config(command=(lambda x, y: lambda: self.on_click(x, y))(i, j))
                self.chessButton[i][j].grid(row=i + 1, column=j)

    def update_time_text_white(self):
        while True:
            if self.model.player == 1:
                minutes = int(self.model.time_white / 60)
                seconds = int(self.model.time_white - minutes * 60.0)
                s_minutes = int(self.model.step_time / 60)
                s_seconds = int(self.model.step_time - s_minutes * 60.0)
                self.time_text_white.set('White Total:%.2d:%.2d  Step:%.2d:%.2d' % (minutes, seconds, s_minutes, s_seconds))
                self.model.time_white += 1
                self.model.step_time += 1
                time.sleep(1)

    def update_time_text_black(self):
        while True:
            if self.model.player == -1:
                minutes = int(self.model.time_black / 60)
                seconds = int(self.model.time_black - minutes * 60.0)
                s_minutes = int(self.model.step_time / 60)
                s_seconds = int(self.model.step_time - s_minutes * 60.0)
                self.time_text_black.set('Black Total: %.2d:%.2d  Step: %.2d:%.2d' % (minutes, seconds, s_minutes, s_seconds))
                self.model.time_black += 1
                self.model.step_time += 1
                time.sleep(1)

    def initialize(self):
        self.model.__init__()
        # initialize components
        self.create_widgets()
        self.time_text_black = StringVar(self, 'Black Total: 00:00  Step: 00:00')
        self.time_text_white = StringVar(self, 'White Total: 00:00  Step: 00:00')
        self.player_text = StringVar(self, 'Current Player: Black')

# 0 for white, 1 for black, 2 for empty
    def get_icon(self, x, y, kind, highlighted):
        if highlighted:
            if x == 0:
                if y == 0:
                    return self.lu_corner_highlighted_icon[kind]
                elif y == 8:
                    return self.ru_corner_highlighted_icon[kind]
                else:
                    return self.up_edge_highlighted_icon[kind]
            elif x == 8:
                if y == 0:
                    return self.ld_corner_highlighted_icon[kind]
                elif y == 8:
                    return self.rd_corner_highlighted_icon[kind]
                else:
                    return self.down_edge_highlighted_icon[kind]
            else:
                if y == 0:
                    return self.left_edge_highlighted_icon[kind]
                elif y == 8:
                    return self.right_edge_highlighted_icon[kind]
                else:
                    return self.cross_highlighted_icon[kind]
        else:
            if x == 0:
                if y == 0:
                    return self.lu_corner_icon[kind]
                elif y == 8:
                    return self.ru_corner_icon[kind]
                else:
                    return self.up_edge_icon[kind]
            elif x == 8:
                if y == 0:
                    return self.ld_corner_icon[kind]
                elif y == 8:
                    return self.rd_corner_icon[kind]
                else:
                    return self.down_edge_icon[kind]
            else:
                if y == 0:
                    return self.left_edge_icon[kind]
                elif y == 8:
                    return self.right_edge_icon[kind]
                else:
                    return self.cross_icon[kind]

    def load_icons(self):
        self.cross_icon.append(PhotoImage(file='white_cross.png'))
        self.cross_highlighted_icon.append(PhotoImage(file='white_cross_highlighted.png'))
        self.down_edge_icon.append(PhotoImage(file='white_down_edge.png'))
        self.down_edge_highlighted_icon.append(PhotoImage(file='white_down_edge_highlighted.png'))
        self.ld_corner_icon.append(PhotoImage(file='white_ld_corner.png'))
        self.ld_corner_highlighted_icon.append(PhotoImage(file='white_ld_corner_highlighted.png'))
        self.left_edge_icon.append(PhotoImage(file='white_left_edge.png'))
        self.left_edge_highlighted_icon.append(PhotoImage(file='white_left_edge_highlighted.png'))
        self.lu_corner_icon.append(PhotoImage(file='white_lu_corner.png'))
        self.lu_corner_highlighted_icon.append(PhotoImage(file='white_lu_corner_highlighted.png'))
        self.rd_corner_icon.append(PhotoImage(file='white_rd_corner.png'))
        self.rd_corner_highlighted_icon.append(PhotoImage(file='white_rd_corner_highlighted.png'))
        self.right_edge_icon.append(PhotoImage(file='white_right_edge.png'))
        self.right_edge_highlighted_icon.append(PhotoImage(file='white_right_edge_highlighted.png'))
        self.ru_corner_icon.append(PhotoImage(file='white_ru_corner.png'))
        self.ru_corner_highlighted_icon.append(PhotoImage(file='white_ru_corner_highlighted.png'))
        self.up_edge_icon.append(PhotoImage(file='white_up_edge.png'))
        self.up_edge_highlighted_icon.append(PhotoImage(file='white_up_edge_highlighted.png'))
        self.cross_icon.append(PhotoImage(file='black_cross.png'))
        self.cross_highlighted_icon.append(PhotoImage(file='black_cross_highlighted.png'))
        self.down_edge_icon.append(PhotoImage(file='black_down_edge.png'))
        self.down_edge_highlighted_icon.append(PhotoImage(file='black_down_edge_highlighted.png'))
        self.ld_corner_icon.append(PhotoImage(file='black_ld_corner.png'))
        self.ld_corner_highlighted_icon.append(PhotoImage(file='black_ld_corner_highlighted.png'))
        self.left_edge_icon.append(PhotoImage(file='black_left_edge.png'))
        self.left_edge_highlighted_icon.append(PhotoImage(file='black_left_edge_highlighted.png'))
        self.lu_corner_icon.append(PhotoImage(file='black_lu_corner.png'))
        self.lu_corner_highlighted_icon.append(PhotoImage(file='black_lu_corner_highlighted.png'))
        self.rd_corner_icon.append(PhotoImage(file='black_rd_corner.png'))
        self.rd_corner_highlighted_icon.append(PhotoImage(file='black_rd_corner_highlighted.png'))
        self.right_edge_icon.append(PhotoImage(file='black_right_edge.png'))
        self.right_edge_highlighted_icon.append(PhotoImage(file='black_right_edge_highlighted.png'))
        self.ru_corner_icon.append(PhotoImage(file='black_ru_corner.png'))
        self.ru_corner_highlighted_icon.append(PhotoImage(file='black_ru_corner_highlighted.png'))
        self.up_edge_icon.append(PhotoImage(file='black_up_edge.png'))
        self.up_edge_highlighted_icon.append(PhotoImage(file='black_up_edge_highlighted.png'))
        self.cross_icon.append(PhotoImage(file='empty_cross.png'))
        self.down_edge_icon.append(PhotoImage(file='empty_down_edge.png'))
        self.ld_corner_icon.append(PhotoImage(file='empty_ld_corner.png'))
        self.left_edge_icon.append(PhotoImage(file='empty_left_edge.png'))
        self.lu_corner_icon.append(PhotoImage(file='empty_lu_corner.png'))
        self.rd_corner_icon.append(PhotoImage(file='empty_rd_corner.png'))
        self.right_edge_icon.append(PhotoImage(file='empty_right_edge.png'))
        self.ru_corner_icon.append(PhotoImage(file='empty_ru_corner.png'))
        self.up_edge_icon.append(PhotoImage(file='empty_up_edge.png'))