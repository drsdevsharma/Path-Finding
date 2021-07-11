import pygame
import math
from queue import PriorityQueue

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("PATH FINDING ALGORITHM")
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORENGE = (255,165,0)
YELLOW = (255,255,0)
PURPLE = (128,0,128)
GREY = (128,128,128)
CYAN = (0,255,255)

class Spot:
    def __init__(self,row,col,width,total_rows): # Initilize the spot
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
    def get_pos(self):      # Get position of mouse
        return self.row, self.col

    def is_closed(self):     # check for closeness
        return self.color == RED
    
    def is_open(self):       # Check for openness
        return self.color == GREEN
    
    def is_start(self):      # Check for Start Node
        return self.color == ORENGE
    
    def is_barrier(self):    # Check for barrier
        return self.color == BLACK

    def is_end(self):        # Check for End Node
        return self.color == CYAN

    def reset(self):         # Reset the Window
        self.color = WHITE

    def make_closed(self):   # Make close the spot
        self.color = RED

    def make_open(self):     # Make open the spot
        self.color = GREEN

    def make_start(self):    # Make starting spot
        self.color = ORENGE

    def make_end(self):     # Make End spot
        self.color = CYAN

    def make_barrier(self): # Make Barrier
        self.color = BLACK

    def make_path(self):    # Show the Path 
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # CHECK FOR DWON
            self.neighbors.append(grid[self.row + 1][self.col]) 

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # CHECK FOR UP
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # CHECK FOR RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # CHECK FOR LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False

def h(p1, p2):
    x1 , y1 = p1
    x2 , y2 = p2
    return abs (x1 - x2) + abs ( y1 - y2)

def make_grid(rows, width):
    grid =[]
    gap = width // rows 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot( i , j , gap , rows)
            grid[i].append(spot)
    return grid

def draw_grid ( win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line( win, GREY, ( 0 ,i*gap ), (width, i*gap))
        for j in range (rows):
            pygame.draw.line( win ,GREY , ( j*gap, 0 ), ( j*gap, width ))
            
def draw ( win, grid, rows, width):
    win.fill ( WHITE)
    for row in grid:
        for spot in row:
            spot.draw( win )
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row , col
 
def reconstruct_path( came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm( draw , grid , START , END):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count ,START)) 
    came_from = {}
    g_score = {spot : float ("inf") for row in grid for spot in row }
    g_score[START] = 0 
    f_score = {spot : float ("inf") for row in grid for spot in row }
    f_score[START] = h( START.get_pos(), END.get_pos())

    open_set_hash = { START }

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == END:
            reconstruct_path (came_from,END,draw)
            END.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[ neighbor ] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h( neighbor.get_pos(),END.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != START:
            current.make_closed()

    return False                

def main( win, width):
    ROWS = 50
    grid = make_grid( ROWS, width)
    START = None
    END = None
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for i in range(ROWS):
            spot = grid [0][i]
            spot2 = grid[i][0]
            spot3 = grid [49][i]
            spot4 = grid[i][49]
            spot3.make_barrier()
            spot4.make_barrier()
            spot.make_barrier()
            spot2.make_barrier()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not START and spot != END:
                    START = spot
                    START.make_start()

                elif not END and spot != START :
                    END = spot
                    END.make_end()

                elif spot != START and spot != END:
                    spot.make_barrier()
                
            elif pygame.mouse.get_pressed()[2]: # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == START:
                    START = None
                elif spot == END:
                    END = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and START and END:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm( lambda: draw( win, grid, ROWS, width), grid,  START, END)
                if event.key == pygame.K_c:
                    START = None
                    END = None
                    grid = make_grid(ROWS,width)    

    pygame.quit()
main(WIN, WIDTH)