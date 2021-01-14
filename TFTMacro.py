import pyautogui
import re

X_DIST = 115
BENCH_X_OFFSET = 300
BENCH_Y_OFFSET = 777
BOARD_X_OFFSET = 415
DRAG_SPEED = 0.1

#Returns parsed location from raw string
#loc: string from user input (e.g. "bench1" returns ("bench", 1))
def parseLoc(loc):
    if re.match("^bench[1-9]$", loc):
        return ("bench", int(loc[5]))
    elif re.match("^[a-d][1-8]$", loc):
        return (loc[0], int(loc[1]))
    else:
        return (None, None)

#Returns pixel location of parsed location
#loc: string from user input (e.g. "bench1" returns (415, 777))
def getLoc(loc):
    (name, tag) = parseLoc(loc)
    if name == None:
        return None
    elif name == "bench":
        return getBenchLoc(tag)
    elif name == "item":
        return getItemLoc(tag)
    else:
        return getBoardLoc(name, tag)


#Returns pixel location of bench column
#col: (int) form of bench column 
#e.g. 1 returns (415, 777)
def getBenchLoc(col):
    return (BENCH_X_OFFSET + X_DIST * col, BENCH_Y_OFFSET)

#Returns pixel location of item number
#num: (int) num of item (e.g. 4)
def getItemLoc(num):
    return None
    
#Returns pixel location of board coordinate
#(row, col): (string, int) form of board coordinate 
#e.g. ("b", 3) returns (760, 680)
def getBoardLoc(row, col):
    rows = {
        "a": 680,
        "b": 600,
        "c": 520,
        "d": 440
    }
    
    offset = 50
    column = BOARD_X_OFFSET + X_DIST * col
    if row == "a" or row == "c":
        column = column + offset
    
    return (column, rows[row])

#Returns true if user input is for moving units
#cmds: list of commands (e.g. ["bench3", "to", "a4"])
def isMove(cmds):
    if len(cmds) == 3:
        if cmds[1] == "to":
            return True
    return False

#Returns true if user input is for items
#cmds: list of commands (e.g. ["item4", "on", "bench2"])
def isItem(cmds):
    if len(cmds) == 3:
        if cmds[1] == "on":
            return True
    return False

#Moves unit from source location to dest location
#source: string name of source location (e.g. "bench4" or "d5")
#dest: string of dest location
def movePiece(source, dest):
    sourcePixel = getLoc(source)
    if sourcePixel is None:
        print("Invalid Location " + source, flush=True)
        return
    destPixel = getLoc(dest)
    if destPixel is None:
        print("Invalid Location " + source, flush=True)
        return

    pyautogui.moveTo(sourcePixel)
    pyautogui.dragTo(destPixel, duration=DRAG_SPEED, button="left")


#Categorizes user input
#input: string of user input (e.g. "bench3 to a4" or "item4 on bench2")
def doCommand(inputs):
    cmds = inputs.split(' ')
    if isMove(cmds):
        movePiece(cmds[0], cmds[2])
    elif isItem(cmds):
        moveItem(cmds[0], cmds[2])


print("TFT Macro activated!")
while True:
    doCommand(input(">"))