import re

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

#Returns true if user input is a sell
#cmds: list of commands (e.g. ["sell", "bench4"])
def isSell(cmds):
    if len(cmds) == 2:
        if re.match("^se?l?l?", cmds[0]):
            return True

    return False

#Returns true if user input is a lock
#cmds: list of commands (e.g. ["lock", "shop"])
def isLock(cmds):
    if len(cmds) > 0:
        if re.match("^lock", cmds[0]):
            return True
        if re.match("^unlock", cmds[0]):
            return True
    return False

#Returns true if user input is a roll
#cmds: list of commands (e.g. ["roll"])
def isRoll(cmds):
    if len(cmds) > 0:
        if re.match("^roll", cmds[0]):
            return True
    return False

#Returns true if user input is a level
#cmds: list of commands (e.g. ["level", "lvl"])
def isLevel(cmds):
    if len(cmds) > 0:
        if re.match("^level", cmds[0]):
            return True
        if re.match("^lvl", cmds[0]):
            return True
        if re.match("^xp", cmds[0]):
            return True
        if re.match("^exp", cmds[0]):
            return True
    return False

#Returns true if user input is a scout
#cmds: list of commands (e.g. ["scout", "left"])
def isScout(cmds):
    if len(cmds) == 2:
        if re.match("^scout", cmds[0]):
            return True

    return False

#Returns true if user input is a reset cam
#cmds: list of commands (e.g. ["reset", "home"])
def isReset(cmds):
    if len(cmds) > 0:
        for cmd in cmds:
            if re.match("reset", cmd):
                return True
            elif re.match("home", cmd):
                return True
            elif re.match("center", cmd):
                return True
            elif re.match("space", cmd):
                return True
    return False

#Returns true if user input is buy
#cmds: list of commands (e.g. ["buy", "shop"])
def isBuy(cmds):
    if len(cmds) > 0:
        if re.match("^shop", cmds[0]):
            return True
        if re.match("^buy", cmds[0]):
            return True
    return False

