# Importing libraries
import pygame
import math
from queue import PriorityQueue

# Setting up the window that the visualiser will be in
width = 800
window = pygame.display.set_mode((width, width))
pygame.display.set_caption("A* Pathfinding Visualiser")

# Setting up colours for later use
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
pink = (153, 0, 153)
yellow = (255,255,0)
grey = (128, 128, 128)

# Allowing the algorithm to interact with the pygame window
class Node:
    def __init__(self, row, col, width, tot_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = white
        self.neighbors = []
        self.width = width
        self.tot_rows = tot_rows

    def get_position(self):
        return self.row, self.col

# Setting up colours for squares in the visualizer
    
    def closedCheck(self):
        return self.colour == red

    def openCheck(self):
        return self.colour == green

    def barrierCheck(self):
        return self.colour == black
    
    def startCheck(self):
        return self.colour == blue

    def endCheck(self):
        return self.colour == pink
    
    def reset(self):
        self.colour = white

    def close(self):
        self.colour = red

    def open(self):
        self.colour = green

    def barrier(self):
        self.colour = black

    def start(self):
        self.colour = blue
    
    def end(self):
        self.colour = pink

    def path(self):
        self.colour = yellow

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))

# This function checks the neighbours of the current node and figures out whether the pathfinding algorithm can move in certain directions or not    
    def neighborUpdate(self, grid):
        self.neighbors = []
        if self.row < self.tot_rows - 1 and not grid[self.row + 1][self.col].barrierCheck(): # Checking if the algorithm can pathfind down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].barrierCheck(): # Checking if the algorithm can pathfind up
            self.neighbors.append(grid[self.row - 1][self.col])  
        if self.col < self.tot_rows - 1 and not grid[self.row][self.col + 1].barrierCheck(): # Checking if the algorithm can pathfind right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].barrierCheck(): # Checking if the algorithm can pathfind right
            self.neighbors.append(grid[self.row][self.col - 1])
    def __lt__(self, other):
        return False

# The heuristic function, figures out distance between 2 points using Manhattan distance ('L' distance) and returns value
def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1-x2) + abs(y1-y2)

# Showing the optimal route to destination after pathfinding is complete
def reconst_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.path()
        draw()

# The A* pathfinding algorithm itself
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_cost = {node: float("inf") for row in grid for node in row}
    g_cost[start] = 0
    f_cost = {node: float("inf") for row in grid for node in row}
    f_cost[start] = heuristic(start.get_position(), end.get_position())
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconst_path(came_from, end, draw)
            end.end()
            return True
        for neighbor in current.neighbors:
            temp_g_cost = g_cost[current] + 1
            if temp_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + heuristic(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_cost[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.open()
        draw()
        if current != start:
            current.close()
    return False
 
# Creates grid on the pygame window
def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

# Draws what was done in the make_grid funciton
def drawGrid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, grey, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(window, grey, (j*gap, 0), (j*gap, width))

# The primary drawing function that fills and redraws every new frame
def drawMain(window, grid, rows, width):
    window.fill(white)
    for row in grid:
        for Node in row:
            Node.draw(window)
    drawGrid(window, rows, width)
    pygame.display.update()

# Gets the position of where the user clicked to feed into the drawing function
def clickPos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# Main function that calls all processes etc.
def main(win, width):
    rows = 50
    grid = makeGrid(rows, width)
    start = None
    end = None
    run = True
    started = False
    while run:
        drawMain(window, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = clickPos(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.start()
                elif not end and node != start:
                    end = node
                    end.end()
                elif node != end and node != start:
                    node.barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = clickPos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.neighborUpdate(grid)
                    algorithm(lambda: drawMain(win, grid, rows, width), grid, start, end)   

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = drawGrid(rows, width)
    pygame.quit()

main(window, width)