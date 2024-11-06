# Lazor Group Project

Welcome to the Lazor Project for EN 540.635 Software Carpentry. This program is designed to solve puzzles from the Lazor smartphone game.

## Code Overview
The following symbols represent elements on the puzzle grid:
- `x`: No block allowed here
- `o`: Block placement allowed here
- `A`: Fixed reflective block
- `B`: Fixed opaque block
- `C`: Fixed refractive block

## Input Requirements
To run the program, a `.bff` file with the following key components is required:
  - **Map grid**: Use the symbols `o`, `x`, `A`, `B`, and `C` to structure the grid. The grid section starts with `GRID START` and ends with `GRID STOP`.
  - **Available blocks**: Specify the count of each block type provided.
  - **Lasers**: Indicate the starting position `(x, y)` and the direction vector `(x, y)` for each laser.
  - **Objective points**: List the coordinates that each laser must reach to solve the puzzle.

### Sample .bff File
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

    
To add your own custom `.bff` file, place it in the project directory and add it to the file selection in the `choose_bff_file` function within the code.<br />
Note that for the xy coordinates, it should be given as if in extended map where the coordinated are multiplied by two. For example, in the above example, the first P coordintate should be translated to 3, 1.5.<br />
In the reduced coordinates, each integer is represented as the center of the block/row/column, and each odd muliple of 0.5 (n.5) is represented as edges. 

## Output
The program will generate a `.txt` file with the solution, displaying the solved grid using the symbols above.

## Usage Instructions
The program should run correctly with any properly formatted `.bff` file. When executed, it will prompt you to select a file, and then it will generate the solution.

## Authors
  Jenny Zhang https://github.com/ztjenny
  
    
    

