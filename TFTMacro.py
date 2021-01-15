import pyautogui
import re
import check
import time

#Constants 

X_DIST = 115
SHOP_X_DIST = 200
BENCH_X_OFFSET = 300
BENCH_Y_OFFSET = 777
SHOP_X_OFFSET = 375
SHOP_Y_OFFSET = 1000
LOCK_LOCATION = (1450, 900)
SELL_LOCATION = (900, 1000)
XP_LOCATION = (365, 960)
ROLL_LOCATION = (365, 1035)
DRAG_SPEED = 0.2
CLICK_DELAY = 0.05
ROWS = {
    "a": (465, 680),
    "b": (420, 600),
    "c": (490, 520),
    "d": (445, 440)
}

class TFTMacro():
    #Returns parsed location from raw string
    #loc: string from user input (e.g. "bench1" returns ("bench", 1))
    def parseLoc(self, loc):
        if re.match("^bench[1-9]$", loc):
            return ("bench", int(loc[5]))
        elif re.match("^[a-d][1-7]$", loc):
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

    def getShopLoc(self, num):
        return (SHOP_X_OFFSET + SHOP_X_DIST * num, SHOP_Y_OFFSET)
        
    #Returns pixel location of board coordinate
    #(row, col): (string, int) form of board coordinate 
    #e.g. ("b", 3) returns (760, 680)
    def getBoardLoc(self, row, col):
        column = ROWS[row][0] + X_DIST * col

        return (column, ROWS[row][1])

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
        pyautogui.dragTo(SELL_LOCATION, duration=DRAG_SPEED, button="left")
        return "Sold unit at " + target

    def buy(self, target):
        if not re.match("^[1-5]+$", target):
            error = "Invalid Shop Target: " + target
            print(error, flush=True)
            return error

        for num in target:    
            targetPixel = self.getShopLoc(int(num))
            pyautogui.moveTo(targetPixel)
            self.click()

        return "Bought unit at shop location(s) " + target

    #Toggles lock shop
    def toggleLock(self):
        pyautogui.moveTo(LOCK_LOCATION)
        self.click()
        return "Toggled shop lock"

    #Presses D to roll
    def roll(self):
        pyautogui.moveTo(ROLL_LOCATION)
        self.click()
        return "Bless rngesus"

    #Presses F to level
    def level(self, num="4"):
        if not num.isdigit():
            error = "Invalid Shop Target: " + target
            print(error, flush=True)
            return error
        num = int(num) // 4
        pyautogui.moveTo(XP_LOCATION)
        for i in range(num):
            self.click()
        return "Wasted " + str(4 * num) + " gold on exp"

    #Scouts either left or right
    def scout(self, place):
        if re.match("^[1-8]$", place):
            return True

    #Presses space to reset camera
    def resetCam(self):
        pyautogui.press('space')

    def click(self):
        pyautogui.mouseDown(button='left')
        time.sleep(CLICK_DELAY)
        pyautogui.mouseUp(button='left')


    #Categorizes user input
    #input: string of user input (e.g. "bench3 to a4" or "item4 on bench2")
    def doCommand(self, inputs):
        cmds = inputs.lower().split(' ')
        print(cmds, flush=True)
        if check.isMove(cmds):
            return self.moveUnit(cmds[0], cmds[2])
        elif check.isItem(cmds):
            return self.moveItem(cmds[0], cmds[2])
        elif check.isSell(cmds):
            return self.sellUnit(cmds[1])
        elif check.isBuy(cmds):
            return self.buy(cmds[1])
        elif check.isLock(cmds):
            return self.toggleLock()
        elif check.isRoll(cmds):
            return self.roll()
        elif check.isLevel(cmds):
            if len(cmds) == 1:
                return self.level()
            else:
                return self.level(cmds[1])
        elif check.isScout(cmds):
            return self.scout(cmds[1])
        elif check.isReset(cmds):
            self.resetCam()
            return "Reset camera"
        else:
            error = "Invalid Command: " + inputs
            print(error, flush=True)
            return error