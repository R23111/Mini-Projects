/**
 * @author Rodrigo Avancini-Lara
 * @email r23111@hotmail.com
 * @create date 02-Sep-2021 09:26:14
 * @modify date 02-Sep-2021 09:26:14
 * @desc a simple term-based minesweep game
 */

//! For an in-depth description of each function, see python program

//! INCLUDES
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

//! DEFINES
#define GRID_SIZE 10
#define MINES 10

//! GRID
int grid[GRID_SIZE][GRID_SIZE];

//! FUNCTIONS
void ClearScreen() { printf("\e[1;1H\e[2J"); }

void PopulateGrid() {
  for (int i = 0; i < GRID_SIZE; i++) {
    for (int j = 0; j < GRID_SIZE; j++) {
      grid[i][j] = 0;
    }
  }
}

void PlaceMines(int x1, int y1) {
  for (int i = 0; i < MINES; i++) {
    int x, y;
    while (1) {
      x = rand() % GRID_SIZE;
      y = rand() % GRID_SIZE;

      if (x == x1 && y == y1)
        continue;

      if (grid[x][y] != -1)
        break;
    }
    grid[x][y] = -1;
  }
}

int PrintGrid() {
  int gameOn = 0;
  for (int x = 0; x < GRID_SIZE; x++) {
    printf("\n");

    for (int y = 0; y < GRID_SIZE; y++) {
      if (grid[x][y] == 0) {
        printf(" [#] ");
        gameOn = 1;
      } else if (grid[x][y] == 10) {
        printf(" [ ] ");
      }

      else if (grid[x][y] == -1)
        printf(" [#] ");
      else
        printf(" [%d] ", grid[x][y]);
    }
  }
  return gameOn;
}

void GameOver(int won) {
  printf("\tG A M E\t\tO V E R\n\n\tY O U");

  if (won) {
    printf("\t\t  W O N\n\n");
  } else {
    printf("\t\tL O S T\n\n");
  }

  for (int x = 0; x < GRID_SIZE; x++) {
    printf("\n");

    for (int y = 0; y < GRID_SIZE; y++) {
      if (grid[x][y] == 0) {
        printf(" [ ] ");
      } else if (grid[x][y] == 10) {
        printf(" [ ] ");
      }

      else if (grid[x][y] == -1)
        printf(" [X] ");
      else if (grid[x][y] == -2)
        printf(" [O] ");
      else
        printf(" [%d] ", grid[x][y]);
    }
  }
}

int TryMine(int x, int y) {
  int numMines = 0;
  if (grid[x][y] == -1) {
    grid[x][y] = -2;
    return 0;
  }

  for (int i = x - 1; i <= x + 1; i++) {
    if (i < 0 || i >= GRID_SIZE)
      continue;
    for (int j = y - 1; j <= y + 1; j++) {
      if (j < 0 || j >= GRID_SIZE)
        continue;

      if (grid[i][j] == -1)
        numMines++;
    }
  }

  if (numMines == 0) {
    grid[x][y] = 10;

    for (int i = x - 1; i <= x + 1; i++) {
      if (i < 0 || i >= GRID_SIZE)
        continue;
      for (int j = y - 1; j <= y + 1; j++) {
        if (j < 0 || j >= GRID_SIZE)
          continue;

        if ((x != i || y != j) && (grid[i][j] != 10) && (grid[i][j] != -1))
          TryMine(i, j);
      }
    }
  } else {
    grid[x][y] = numMines;
  }

  return 1;
}

int main() {
  srand(time(NULL));
  int gameOn = 1;
  int firstLoop = 1;
  int won = 1;

  //! GAMELOOP
  while (gameOn) {
    int x = -1;
    int y = -1;
    while (1) {
      printf("x = ");
      scanf("%d", &y);
      printf("y = ");
      scanf("%d", &x);
      if (x >= 0 && x < GRID_SIZE && y >= 0 && y < GRID_SIZE)
        break;
    }
    if (firstLoop) {
      PlaceMines(x, y);
      firstLoop = 0;
    }
    gameOn = TryMine(x, y);
    if (!gameOn) {
      won = 0;
      break;
    }

    ClearScreen();
    gameOn = PrintGrid();
    printf("\n");
  }

  GameOver(won);

  return 0;
}