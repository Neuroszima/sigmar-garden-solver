# sigmar-garden-solver
Everything related to sigmar garden minigame, playable in console as well as solvable through console and direct screen capture

This project starts as Python-mainly, however in future the Zig programming language 
code will be added to aid solution finding speed.

### Requirements

This project will be maintained under Python version 3.12, as well as Zig version 0.15.1. The rest of the
requirements will be included in project-specific requirements.txt file. The requirements.txt will hold all the 
dependencies for the Python side of the project.

### Basic info and roadmap

Project wil be split in 3 parts - 
1. Console-like game with inputs/outputs by the user
2. Visual inspector, capable of locating the board space in the image/screen dump and recovering its 
    contents into program-readable format for other parts of the project.
3. Solver/Checker which either consumes a board prepared by a console game, or direct dump from screen by performing
    the visual check mentioned in previous point.

The solver part in the end will be prepared using Zig programming language, to faster iterate through solution space.

As I have just started learning Zig, this will take a while to actually get some sensible results from solver part
in that particular language. For now, the python side with simple board (reduced pieces and board size compared 
to original) will be added, and then the visual side/OCR/scanning module will be prepared.

Roadmap below:
