import tkinter as tk
from tkinter import messagebox
import copy

class GameOfLifeGUI:
    def __init__(self):
        ## Init
        self.root = tk.Tk()
        self.root.geometry('1366x768')
        self.root.title('Conway\'s Game of Life Simulator')
        self.font = ('Arial', 18)
        self.grid_sizes = [1,2,3,4,5,6,10,12,15,20,25,30,50,60,75,100,150,300]
        self.ht, self.wd = 600, 900
        self.border_size = 3
        self.colour_on, self.colour_off = 'dark grey', 'white'
        
        self.gs = GameOfLife()
        self.start_cells = set([])
        self.change_start_cells = False
        
        ## Creating Widgets
        # Variables
        self.zoom_level = tk.IntVar(self.root, value=12)
        self.speed_level = 1
        self.speed = 1 #Frames per second
        self.max_iter = tk.StringVar(self.root, value='5')
        self.max_iter.trace('w', lambda name, index, mode, var=self.max_iter: self.check_int(var))
        
        # Widgets
        self.fun_frame = tk.Frame(self.root)
        
        self.var_frame = tk.Frame(self.fun_frame)
        
        self.zoom_title = tk.Label(self.var_frame, text='Zoom:', font=self.font)
        self.zoom_out_btn = tk.Button(self.var_frame, command=self.zoom_out,
                                      text='-', font=self.font)
        self.zoom_in_btn = tk.Button(self.var_frame, command=self.zoom_in,
                                      text='+', font=self.font)
        
        self.speed_title = tk.Label(self.var_frame, text='Speed (fps):', font=self.font)
        self.speed_label = tk.Label(self.var_frame, text=self.speed, font=self.font)
        self.speed_down = tk.Button(self.var_frame, command=self.speed_down,
                                    text='-', font=self.font)
        self.speed_up = tk.Button(self.var_frame, command=self.speed_up,
                                  text='+', font=self.font)
        
        self.max_iter_title = tk.Label(self.var_frame, text='Max No. of Iterations:', font=self.font)
        self.max_iter_entry = tk.Entry(self.var_frame, textvariable=self.max_iter, font=self.font,
                                       width=5, justify=tk.CENTER)
        
        self.board = tk.Canvas(self.root, bd=self.border_size, bg='black',
                               height=self.ht,
                               width=self.wd)
        
        self.resize_grid()
        
        self.fun_bar = tk.Frame(self.fun_frame)
        self.start_btn = tk.Button(self.fun_bar, command=self.start_sim,
                                   text='Start', font=self.font)
        self.next_btn = tk.Button(self.fun_bar, command=self.next_turn,
                                  text='Next', font=self.font)
        self.reset_btn = tk.Button(self.fun_bar, command=self.reset,
                                   text='Reset', font=self.font)
        self.clear_all_btn = tk.Button(self.fun_bar, command=self.clear_all,
                                       text='Clear All', font=self.font)
        
        ## Functionality
        self.create_binding()
        
        ## Displaying Widgets
        self.fun_frame.pack(side=tk.LEFT, padx=20)
        
        self.var_frame.grid(row=0, column=0, pady=20)
        
        self.zoom_title.grid(row=0, column=0, columnspan=2, padx=5, sticky=tk.W)
        self.zoom_out_btn.grid(row=0, column=2, padx=5)
        self.zoom_in_btn.grid(row=0, column=3, padx=5)
        
        self.speed_title.grid(row=1, column=0, padx=5, sticky=tk.W)
        self.speed_label.grid(row=1, column=1, padx=5)
        self.speed_down.grid(row=1, column=2, padx=5)
        self.speed_up.grid(row=1, column=3, padx=5)
        
        self.max_iter_title.grid(row=2, column=0, columnspan=2, padx=5, sticky=tk.W)
        self.max_iter_entry.grid(row=2, column=2, columnspan=2, padx=5)
        
        self.board.pack(side=tk.RIGHT, padx=20)
        
        self.fun_bar.grid(row=1, column=0, pady=20)
        self.start_btn.grid(row=0, column=0, padx=5)
        self.next_btn.grid(row=0, column=1, padx=5)
        self.reset_btn.grid(row=0, column=2, padx=5)
        self.clear_all_btn.grid(row=0, column=3, padx=5)
        
        ## Main Loop
        self.root.mainloop()

    #####
    
    def resize_grid(self):
        self.board.delete('all')
        self.grid_size = self.grid_sizes[self.zoom_level.get()]
        self.cells = []
        self.n_ht = int(self.ht/self.grid_size)
        self.n_wd = int(self.wd/self.grid_size)
        
        start_i, start_j = self.border_size+1, self.border_size+1
        for i in range(self.n_ht):
            row_rects = []
            next_i = start_i+self.grid_size
            for j in range(self.n_wd):
                next_j = start_j+self.grid_size
                rect = self.board.create_rectangle(start_j, start_i, next_j, next_i,
                                                   fill=self.colour_off, outline='light grey', width=1)
                start_j = next_j
                row_rects.append(rect)
            start_i = next_i
            start_j = self.border_size+1
            self.cells.append(row_rects)
    
    def create_binding(self):
        self.board.bind('<Button-1>', lambda event: self.toggle(event))
        
    def toggle(self, event):
        if self.change_start_cells:
            self.start_cells = copy.copy(self.gs.cells)
        i = (event.y-self.border_size-1)//self.grid_size
        j = (event.x-self.border_size-1)//self.grid_size
        if i >= 0 and j >= 0 and i < len(self.cells) and j < len(self.cells[0]):
            rect = self.cells[i][j]
            if self.board.itemcget(rect, 'fill') == self.colour_off:
                self.board.itemconfig(rect, fill=self.colour_on)
                self.start_cells.add((i,j))
                self.gs.cells.add((i,j))
            else:
                self.board.itemconfig(rect, fill=self.colour_off)
                self.start_cells.remove((i,j))
                self.gs.cells.remove((i,j))

    def start_sim(self):
        self.board.unbind('<Button-1>')
        self.start_btn['text'] = 'Stop'
        self.start_btn['command'] = self.stop_sim
        self.next_turn_updater()
    
    def next_turn_updater(self):
        if self.gs.terminate or self.gs.turn >= int(self.max_iter.get()):
            self.stop_sim()
        else:
            self.next_turn()
            self.root.after(int(1000/self.speed), self.next_turn_updater)
    
    def stop_sim(self):
        self.gs.terminate = True
        self.start_btn['text'] = 'Start'
        self.start_btn['command'] = self.start_sim
        self.start_btn['state'] = tk.DISABLED
        self.create_binding()
        if self.gs.period:
            print(self.gs.period)
    
    def next_turn(self):
        self.gs.move()
        self.update()
        self.change_start_cells = True
    
    def reset(self):
        self.change_start_cells = False
        self.start_btn['state'] = tk.NORMAL
        self.gs = GameOfLife()
        self.gs.init_cells(self.start_cells)
        self.displace_cells()
        self.refresh()
    
    def clear_all(self):
        self.start_cells = set([])
        self.reset()
    
    def update(self):
        for (i,j) in self.gs.died_cells:
            if i >= 0 and j >= 0 and i < len(self.cells) and j < len(self.cells[0]):
                self.board.itemconfig(self.cells[i][j], fill=self.colour_off)
        for (i,j) in self.gs.born_cells:
            if i >= 0 and j >= 0 and i < len(self.cells) and j < len(self.cells[0]):
                self.board.itemconfig(self.cells[i][j], fill=self.colour_on)
    
    def refresh(self):
        for i, row_rect in enumerate(self.cells):
            for j, rect in enumerate(row_rect):
                if (i,j) in self.gs.cells:
                    self.board.itemconfig(rect, fill=self.colour_on)
                else:
                    self.board.itemconfig(rect, fill=self.colour_off)

    def check_int(self, var):
        s = var.get()
        if s and s[-1] not in '0123456789':
            tk.messagebox.showerror('Max No. of Turns', 'Error: Please only enter a positive integer')
            var.set(s[:-1])
    
    #####
    
    def displace_cells(self):
        self.i_c, self.j_c = self.gs.get_centroid()
        self.i_disp = self.n_ht//2 - self.i_c
        self.j_disp = self.n_wd//2 - self.j_c
        self.start_cells = set((i+i_disp,j+j_disp) for i,j in self.start_cells)
        self.gs.cells = set((i+i_disp,j+j_disp) for i,j in self.gs.cells)
    
    def zoom_in(self):
        self.zoom_level.set(min(self.zoom_level.get()+1, len(self.grid_sizes)-1))
        self.resize_grid()
        self.displace_cells()
        self.refresh()
    
    def zoom_out(self):
        self.zoom_level.set(max(self.zoom_level.get()-1, 0))
        self.resize_grid()
        self.displace_cells()
        self.refresh()
    
    def refresh_speed(self):
        if self.speed_level > 0:
            self.speed = self.speed_level
            self.speed_label['text'] = self.speed
        elif self.speed_level < -1:
            self.speed = 1/-self.speed_level
            self.speed_label['text'] = f'1/{-self.speed_level}'
        else:
            self.speed = 0
            self.speed_label['text'] = self.speed
    
    def speed_up(self):
        self.speed_level += 1
        if self.speed_level == -1:
            self.speed_level = 1
        self.refresh_speed()
        
    def speed_down(self):
        self.speed_level -= 1
        if self.speed_level == 0:
            self.speed_level = -2
        self.refresh_speed()

##########

class GameOfLife:
    def __init__(self, survival_n = (2,3), birth_n = (3,), max_mem = 100):
        self.survival_n = survival_n
        self.birth_n = birth_n
        self.turn = 0
        self.cells = set([])
        self.stack = set([])
        self.max_mem = max_mem
        self.mem = []
        self.terminate = False
        self.period = None
    
    def init_cells(self, coords):
        self.cells = coords
        self.mem.append(self.cells)

    def count_neighbours(self, x, y):
        n = 0
        for cell in self.cells: #checks that: x coord is within range, y coord is within range, and neighbour is not itself
            if cell[0] <= x+1 and cell[0] >= x-1 and \
            cell[1] <= y+1 and cell[1] >= y-1 and \
            (cell[0] != x or cell[1] != y):
                n += 1
        return n

    def get_adj_coords(self, x, y):
        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:
                    self.stack.add((x+i, y+j))
        self.stack = self.stack - self.cells #stack should contain only empty spaces

    def get_centroid(self):
        if len(self.cells) == 0:
            return 0,0
        else:
            i_c, j_c = 0,0
            for i,j in self.cells:
                i_c += i
                j_c += j
            i_c /= len(self.cells)
            j_c /= len(self.cells)
            return round(i_c), round(j_c)
    
    def move(self):
        self.turn += 1
        new_cells = set([])
        self.died_cells = set([])
        self.born_cells = set([])
        for x,y in self.cells:
            self.get_adj_coords(x,y)
            n = self.count_neighbours(x,y)
            if n in self.survival_n:
                new_cells.add((x,y))
            else:
                self.died_cells.add((x,y))
        for x,y in self.stack:
            n = self.count_neighbours(x,y)
            if n in self.birth_n:
                new_cells.add((x,y))
                self.born_cells.add((x,y))
        if new_cells in self.mem:
            self.terminate = True
            self.period = len(self.mem) - self.mem.index(new_cells)
        self.cells = copy.copy(new_cells)
        self.stack = set([])
        self.mem.append(self.cells)
        if len(self.mem) > self.max_mem:
            del self.mem[0]