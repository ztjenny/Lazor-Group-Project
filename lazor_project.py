'''
Author: Jiale Huang
        Jenny Zhang

Last Modified: Nov 6, 2024


Code Overview::
The following symbols represent elements on the puzzle grid:
x: No block allowed here
o: Block placement allowed here
A: Fixed reflective block
B: Fixed opaque block
C: Fixed refractive block

Input Requirements:
To run the program, a `.bff` file with the following key components is required:
  -Map grid: Use the symbols `o`, `x`, `A`, `B`, and `C` to structure the grid. The grid section starts with `GRID START` and ends with `GRID STOP`.
  -Available blocks: Specify the count of each block type provided.
  -Lasers: Indicate the starting position `(x, y)` and the direction vector `(x, y)` for each laser.
  -Objective points: List the coordinates that each laser must reach to solve the puzzle.

Sample .bff File
Here’s what a sample `.bff` file might look like:

    GRID START
    o o o o o
    o o o o o
    o o x o o
    o o o o o
    o o o o o
    GRID STOP
    
    A 8
    
    L 2 1 1 1
    L 9 4 -1 1
    
    P 6 3
    P 6 5
    P 6 7
    P 2 9
    P 9 6

Note:
  - To add your own custom `.bff` file, place it in the project directory and add it to the file selection in the `choose_bff_file` function within the code.
  - Note that for the xy coordinates, it should be given as if in extended map where the coordinated are multiplied by two. 
          For example, in the above example, the first P coordintate should be translated to (3, 1.5).
  - In the reduced coordinates, each integer is represented as the center of the block/row/column, and each odd muliple of 0.5 (n.5) is represented as edges. 
  - The .bff files include two testing .bff files which are invalid maps, named "invalid_grir.bff" and "no_blocks.bff". The rest are the maps used for this program.




Output:
The program will generate a `.txt` file with the solution, displaying the solved grid using the symbols above.

Usage Instructions:
The program should run correctly with any properly formatted `.bff` file. When executed, it will prompt you to select a file, and then it will generate the solution.

Authors:
  Jenny Zhang https://github.com/ztjenny
  Jiale Huang https://github.com/joe0629
'''


from collections import Counter
from itertools import combinations
import unittest
import time


class Grid:
    '''
    This class exhausts all possible configurations on the current grid with all available blocks.
    '''

    def __init__(self, g):
        '''
        Initializes a new instance of the class with the rows and columns from the imported grid 'g'.
        '''
        self.grid = g
        self.row = len(g)
        self.col = len(g[0])

    def place_block(self, reflect, opaque, refract):
        '''
        Converts the original 2D grid list to a 1D list to simplify permutation generation.
        '''
        oneD_grid = [j for i in self.grid for j in i]
        return self.generate_placements(reflect.num, opaque.num, refract.num, oneD_grid)

    def generate_placements(self, num_reflect, num_opaque, num_refract, base_grid):
        '''
        Generates all possible configurations of blocks in the grid.
        '''
        grid_indices = [i for i, v in enumerate(base_grid) if v == 'o']
        all_configs = []

        for reflect_positions in combinations(grid_indices, num_reflect):
            remaining_indices_after_reflect = [
                i for i in grid_indices if i not in reflect_positions]

            for opaque_positions in combinations(remaining_indices_after_reflect, num_opaque):
                remaining_indices_after_opaque = [
                    i for i in remaining_indices_after_reflect if i not in opaque_positions]

                for refract_positions in combinations(remaining_indices_after_opaque, num_refract):
                    grid = base_grid[:]
                    for r in reflect_positions:
                        grid[r] = 'A'
                    for b in opaque_positions:
                        grid[b] = 'B'
                    for y in refract_positions:
                        grid[y] = 'C'

                    converted_2D_grid = [
                        grid[i*self.col:(i+1)*self.col] for i in range(self.row)]
                    all_configs.append(converted_2D_grid)

        return all_configs


class Laser:
    '''
    Simulates the behavior of lasers based on interactions with blocks.
    '''

    def __init__(self, x, y, vx, vy):
        self.x = int(x)
        self.y = int(y)
        self.vx = int(vx)
        self.vy = int(vy)
        self.path = []
        self.sub = []

    def chk_nonstop(self, grid):
        return 0 <= self.x < len(grid[0]) and 0 <= self.y < len(grid)

    def go(self, grid):
        self.path.append((self.x, self.y))
        current_pos = grid[self.y][self.x]
        if current_pos == 's':
            temp_x = self.x + (self.vx if self.x % 2 == 0 else 0)
            temp_y = self.y + (self.vy if self.x % 2 != 0 else 0)
            block = grid[temp_y][temp_x] if 0 <= temp_x < len(grid[0]) and 0 <= temp_y < len(grid) else None
            self.interaction(block)
        self.x += self.vx
        self.y += self.vy

    def interaction(self, block):
        if block == 'B':
            self.vx = self.vy = 0
        elif block == 'A':
            self.vx, self.vy = (-self.vx, self.vy) if self.x % 2 == 0 else (self.vx, -self.vy)
        elif block == 'C':
            new_laser = Laser(self.x, self.y, -self.vx if self.x % 2 == 0 else self.vx, self.vy if self.x % 2 == 0 else -self.vy)
            self.sub.append(new_laser)

    def chk_sub(self):
        return bool(self.sub)

    def clear_sub(self):
        self.sub.clear()

    def chk_loop(self):
        return Counter(self.path).most_common(1)[0][1] > 3 if self.path else False

    def copy(self):
        return Laser(self.x, self.y, self.vx, self.vy)


class Block:
    def __init__(self, block_type):
        self.block_type = block_type


class Opaque_block(Block):
    def __init__(self, n=0):
        super().__init__('B')
        self.num = n


class Reflect_block(Block):
    def __init__(self, n=0):
        super().__init__('A')
        self.num = n


class Refract_block(Reflect_block):
    def __init__(self, n=0):
        super().__init__('C')
        self.num = n


def find_elements(matrix, value):
    return [(i, j) for i, row in enumerate(matrix) for j, elem in enumerate(row) if elem == value]


def detail(grid):
    old_row, old_col = len(grid), len(grid[0])
    new_row, new_col = 2 * old_row + 1, 2 * old_col + 1
    new_grid = [['o' for _ in range(new_col)] for _ in range(new_row)]

    for element in ['x', 'B', 'A', 'C']:
        for row, col in find_elements(grid, element):
            temp_row, temp_col = 2 * row + 1, 2 * col + 1
            new_grid[temp_row][temp_col] = element
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_grid[temp_row + dr][temp_col + dc] = 's'
    return new_grid


def overview(grid):
    old_row, old_col = len(grid), len(grid[0])
    new_row, new_col = (old_row - 1) // 2, (old_col - 1) // 2
    new_grid = [['o' for _ in range(new_col)] for _ in range(new_row)]

    for element in ['x', 'B', 'A', 'C']:
        for row, col in find_elements(grid, element):
            temp_row, temp_col = (row - 1) // 2, (col - 1) // 2
            new_grid[temp_row][temp_col] = element
    return new_grid

def is_valid_grid(grid):
    # Check if all rows have the same length
    row_length = len(grid[0])
    if any(len(row) != row_length for row in grid):
        return False

    # Check for invalid characters (assuming only 'x', 'o', 'r', 'b' are allowed)
    valid_chars = {'x', 'o', 'A', 'B', 'C'}
    for row in grid:
        if any(cell not in valid_chars for cell in row):
            return False

    # Additional checks (e.g., for start/end points, out-of-bounds errors)
    return True





class Game:
    '''
    Reads the .bff file, lists all block configurations, and checks if lasers reach target points.
    '''
    def __init__(self, filename):
        self.file = filename.split(".")[0]
        with open(filename, "r") as f:
            lines = f.readlines()

        self.lasers = []
        self.points = []
        self.reflect_blocks = Reflect_block()
        self.opaque_blocks = Opaque_block()
        self.refract_blocks = Refract_block()

        grid_found = False
        block_found = False
        objective_found = False
        laser_found = False

        # Initialize g as an empty list to avoid UnboundLocalError
        g = []

        for line in lines:
            if line.startswith('GRID START'):
                grid_found = True
                for line in lines[lines.index(line) + 1:]:
                    if line.startswith('GRID STOP'):
                        break
                    g.append(line.rstrip().split())
                self.grid1 = Grid(g)
            elif line.startswith('L'):
                laser_found = True
                l = line[1:].split()
                self.lasers.append(Laser(*l))
            elif line.startswith('P'):
                objective_found = True
                p = line[1:].split()
                self.points.append((int(p[0]), int(p[1])))
            elif line.startswith('A'):
                block_found = True
                try:
                    self.reflect_blocks.num = int(line[2])
                except:
                    pass
            elif line.startswith('B'):
                block_found = True
                try:
                    self.opaque_blocks.num = int(line[2])
                except:
                    pass
            elif line.startswith('C'):
                block_found = True
                try:
                    self.refract_blocks.num = int(line[2])
                except:
                    pass

        # Check if the grid was found and validate it
        if not grid_found or not g:
            raise ValueError("No valid grid found.")

        # Check if the grid is valid
        if not is_valid_grid(g):
            raise ValueError("Invalid grid.")

        # Check for missing blocks and objectives
        if not block_found:
            raise ValueError("No blocks found.")
        if not objective_found:
            raise ValueError("No objective points found.")
        if not laser_found:
            raise ValueError("No lasers found.")


    def run(self):
        maps = self.grid1.place_block(self.reflect_blocks, self.opaque_blocks, self.refract_blocks)
        for m in maps:
            new_m = detail(m)
            all_paths = []

            for laser in [laser.copy() for laser in self.lasers]:
                while laser.chk_nonstop(new_m) and not laser.chk_loop():
                    laser.go(new_m)
                    if laser.chk_sub():
                        self.lasers.append(laser.sub[0])
                        laser.clear_sub()
                all_paths.extend(laser.path)

            if all(point in all_paths for point in self.points):
                answer = overview(new_m)
                with open(f"{self.file}_answer.txt", 'w') as f:
                    for row in answer:
                        f.write('\t'.join(row) + '\n')
                break






class TestGame(unittest.TestCase):
    def test_invalid_grid(self):
        with self.assertRaises(ValueError):  # Catch the ValueError
            game_instance = Game('invalid_grid.bff')  # Or use a mock for testing

    def test_missing_blocks(self):
        with self.assertRaises(ValueError):
            game = Game('no_blocks.bff')  # Test when no block data is in the .bff file'''






if __name__ == '__main__':
    game = Game('yarn_5.bff')
    start_time = time.time()
    game.run()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    unittest.main(argv=[''], exit=False)
