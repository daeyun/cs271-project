# Othello Game AI

Our implementation can be found in this file: [othello-cpp/othello.h](https://github.com/daeyun/cs271-project/blob/master/othello-cpp/othello.h)

The Python code calls the C++ implementation through [ctypes](https://docs.python.org/3/library/ctypes.html).

### Group members:

- Ananth Gottumukkala
- Avinash Nath Aita
- Daeyun Shin


### Video:

https://www.youtube.com/watch?v=1JEZx0B54zo


### Instructions

1. Run the ./othello-cpp/build_all.sh script.  It will build the C++ code as a .so library file using CMake.  Requires CMake, OpenMP, Catch (a C++ unit testing framework) installed. We only tested on Ubuntu 18.04.

2. Install Python dependencies: numpy, matplotlib.

3. Run  python run_evaluation.py  to run runtime and winrate evaluation.

4. Run  python run_manual_play.py  to play against GUI or CLI  (comment out the main_gui() function if you want CLI only).
