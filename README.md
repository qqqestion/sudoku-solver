# Sudoku solver

## Run

```
python3 main.py [-f filename]
```

- With -f argument can be specified file where sudoku puzzle contains. 

## Solving method

I used human like method of solving such as hidden singles and naked singles, 
etc. But when those methods doesn't work programm randomly chooses a cell and 
puts a number there, if it helps and its' valid, it keep solving, if not chooses
another cell.