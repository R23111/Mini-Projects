# 
#  @author Rodrigo Avancini-Lara
#  @email r23111@hotmail.com
#  @create date 02-Sep-2021 08:29:02
#  @modify date 02-Sep-2021 08:29:02
#  @desc a simple term-based minesweep game
#

#! IMPORTS
#region imports

import random as rnd

#endregion

#! SET VARIABLES
#region Vars

mines = 10
GRID_SIZE = 10
grid = []
game_on = True
first_loop = True
won = True

#endregion

#! Functions
#region Functions

def clear_screen():
    # Clear the screen "ctrl + l" 
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')
    
# Return "emojified" number    
def set_number(n):
    return ["1️⃣ ", "2️⃣ ", "3️⃣ ", "4️⃣ ", "5️⃣ ", "6️⃣ ", "7️⃣ ", "8️⃣ "][n-1]

# prints the grid
def print_grid():
    game_on = False
    
    print("\t", end=' ')
    for i in range(GRID_SIZE):
        print(f"{i} ", end=' ')
    print('\n')
    
    for x in range(len(grid[1])):  
        print("", end=f'\n{x}\t')      
        for y in range(len(grid[0])):
            if(grid[x][y] == 0):        # Check for non-mine cells
                print(f"⬛", end=' ')
                game_on = True          # If there is a non-mine not explored, game keeps going
                
            elif(grid[x][y] == -1):     # Check for mine cells 
                print(f"⬛", end=' ')    
                
            else:                       # Check for explored cells
                print(f"{grid[x][y]}", end=' ')
    print('\n')
    
    return game_on                      # if no mine was found,return False (game-over, player won), else game_on! (True)
     
# place the mines on the grid
def place_mines(x1, y1):
    for m in range(mines):
        while(True):
            x = rnd.randint(0, GRID_SIZE-1)
            y = rnd.randint(0, GRID_SIZE-1)
            if([x, y] == [x1, y1]): continue    # don't allow to mine be set on the player's first move
            if(grid[x][y] != -1): break         # if already hasn't a mine there, good to go
        grid[x][y] = -1

def try_mine(x, y):
    num_mines = 0
        
    if grid[x][y] == -1:
        grid[x][y] = "💥"
        print("GAME OVER")
        return False
    
    # Check for nearby mines
    for i in range (x-1, x+2, 1):
        if(i < 0 or i > GRID_SIZE-1): continue        # Check if out of scope
        for j in range(y-1, y+2, 1):
            if(j < 0 or j > GRID_SIZE-1): continue    # Check if out of scope
            if(grid[i][j] == -1):
                num_mines += 1
        
    if(num_mines == 0):         
        grid[x][y] = "⬜"
        
        # if there is no mine nearby, search until find on those cells (recursively)
        for i in range (x-1, x+2, 1):
            if(i < 0 or i > GRID_SIZE-1): continue        # Check if out of scope
            for j in range(y-1, y+2, 1):
                if(j < 0 or j > GRID_SIZE-1): continue
                if ([x, y] != [i, j] and grid[i][j] != "⬜" and grid[i][j] != -1):   # Check if out of scope and if its not itself
                    try_mine(i,j)

    else:
        grid[x][y] = set_number(num_mines)

    return True

# Populate the grid with empty cells
def populate_grid():
    for i in range(GRID_SIZE):
        grid.append([])    
        for j in range(GRID_SIZE):
            grid[i].append(0)

# Game-Over Screen    
def end_game():
    clear_screen()
    print("\tG A M E\t\tO V E R\n\n\tY O U", end='')
    if(won):
        print('\t\t  W O N', end='\n\n')
    else:
        print('\t\tL O S T', end='\n\n')
    for x in range(len(grid[1])):
        for y in range(len(grid[0])):
            if(grid[x][y] == 0):
                    print(f" ⬜ ", end='')
            elif(grid[x][y] == -1):
                print(f" 💣 ", end='')
            else:
                print(f" {grid[x][y]} ", end='')
        print("")

#endregion

#! Pre-Game
#region Pre-game

populate_grid()
clear_screen()
print_grid()

#endregion

#! GAME LOOP
#region Game Loop

while(game_on):
    while(True):       
        
        y = input("x =")
        x = input("y =")
        
        # Check if int
        try:        
            x = int(x)
            y = int(y)
        except:
            continue
        
        # Check if out of scope
        if(x >= 0 and x < GRID_SIZE and y >= 0 and y < GRID_SIZE): 
            break
    
    # Generate mines AFTER first round, so the player don't lose on start
    if(first_loop):
        place_mines(x, y)
        first_loop = False
    
    game_on = try_mine(x, y)
    
    # Check if lost due to a mine
    if(not game_on):
        won = False
        break
   
    clear_screen()
    
    game_on = print_grid()
        
end_game()

#endregion