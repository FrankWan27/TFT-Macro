import pyautogui
import re
import check

#Constants 

X_DIST = 115
BENCH_X_OFFSET = 300
BENCH_Y_OFFSET = 777
BOARD_X_OFFSET = 415
LOCK_LOCATION = (123, 123)
DRAG_SPEED = 0.1


class TFTMacro():
    #Returns parsed location from raw string
    #loc: string from user input (e.g. "bench1" returns ("bench", 1))
    def parseLoc(self, loc):
        if re.match("^bench[1-9]$", loc):
            return ("bench", int(loc[5]))
        elif re.match("^[a-d][1-8]$", loc):
            return (loc[0], int(loc[1]))
        else:
            return (None, None)

    #Returns pixel location of parsed location
    #loc: string from user input (e.g. "bench1" returns (415, 777))
    def getLoc(self, loc):
        (name, tag) = self.parseLoc(loc)
        if name == None:
            return None
        elif name == "bench":
            return self.getBenchLoc(tag)
        elif name == "item":
            return self.getItemLoc(tag)
        else:
            return self.getBoardLoc(name, tag)


    #Returns pixel location of bench column
    #col: (int) form of bench column 
    #e.g. 1 returns (415, 777)
    def getBenchLoc(self, col):
        return (BENCH_X_OFFSET + X_DIST * col, BENCH_Y_OFFSET)

    #Returns pixel location of item number
    #num: (int) num of item (e.g. 4)
    def getItemLoc(self, num):
        return None
        
    #Returns pixel location of board coordinate
    #(row, col): (string, int) form of board coordinate 
    #e.g. ("b", 3) returns (760, 680)
    def getBoardLoc(self, row, col):
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

    #Moves unit from source location to dest location
    #source: string name of source location (e.g. "bench4" or "d5")
    #dest: string of dest location
    def moveUnit(self, source, dest):
        sourcePixel = self.getLoc(source)
        if sourcePixel is None:
            error = "Invalid Location: " + source
            print(error, flush=True)
            return error
        destPixel = self.getLoc(dest)
        if destPixel is None:
            error = "Invalid Location: " + dest
            print(error, flush=True)
            return error

        pyautogui.moveTo(sourcePixel)
        pyautogui.dragTo(destPixel, duration=DRAG_SPEED, button="left")
        return "Moved unit from " + source + " to " + dest

    #Sells unit at target location (presses E)
    #target: string name of target location (e.g. "bench4")
    def sellUnit(self, target):
        targetPixel = self.getLoc(target)
        if targetPixel is None:
            error = "Invalid Location: " + target
            print(error, flush=True)
            return error

        pyautogui.moveTo(targetPixel)
        pyautogui.press('e')
        return "Sold unit at " + target

    #Toggles lock shop
    def toggleLock(self):
        pyautogui.moveTo(LOCK_LOCATION)
        pyautogui.click()
        return "Toggled shop lock"

    #Presses D to roll
    def roll(self):
        pyautogui.press('d')
        return "Bless rngesus"

    #Presses F to level
    def level(self):
        pyautogui.press('f')
        return "Wasted 4 gold on exp"

    #Scouts either left or right
    def scout(self, direction):
        if re.match("left", direction):
            pyautogui.press('q')
            return "Scout 1 left"
        elif re.match("right", direction):
            pyautogui.press('e')
            return "Scout 1 right"
        return "Invalid direction to scout"

    #Presses space to reset camera
    def resetCam(self):
        pyautogui.press('space')


    #Categorizes user input
    #input: string of user input (e.g. "bench3 to a4" or "item4 on bench2")
    def doCommand(self, inputs):
        cmds = inputs.lower().split(' ')
        if check.isMove(cmds):
            return self.moveUnit(cmds[0], cmds[2])
        elif check.isItem(cmds):
            return self.moveItem(cmds[0], cmds[2])
        elif check.isSell(cmds):
            return self.sellUnit(cmds[1])
        elif check.isLock(cmds):
            return self.toggleLock()
        elif check.isRoll(cmds):
            return self.roll()
        elif check.isLevel(cmds):
            return self.level()
        elif check.isScout(cmds):
            return self.scout(cmds[1]):
        elif check.isReset(cmds):
            self.resetCam()
            return "Reset camera"
        else:
            error = "Invalid Command: " + inputs
            print(error, flush=True)
            return error