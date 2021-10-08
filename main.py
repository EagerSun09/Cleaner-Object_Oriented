##################################################################################################
# Name: Yige Sun
# CS - 160 - Artificial Intelligence
# HomeWork 1 - Behavior Tree
##################################################################################################
# Node status is defined at line 114
# To modify which task will be performed, please modify the settings in Cleaner.run() at line 554
##################################################################################################
import time
import random
import math

cleanerState= {
    "BATTERY_LEVEL": 25,
    "SPOT": False,
    "SPOT_LOCATION": (3.0, 7.0),
    "GENERAL": False,
    "DUSTY_SPOT": False,
    "DUSTY_SPOT_LOCATION": (0.0, -4.0),
    "HOME_PATH": [],
    "LOCATION": (-3.0, 5.0),
    "FACING": (0, 1)
}

def updateBattery(conditions, precent):
    battery = conditions["BATTERY_LEVEL"]
    battery += precent
    if battery > 100:
        battery = 100
    elif battery < 0:
        battery = 0
    conditions.update({"BATTERY_LEVEL": battery})
    return True

def changeLocation(cleanerState, degreeHorizon, degreeVertical):
    randomHorizon = round(random.random()-0.5, 1) * degreeHorizon
    randomVertical = round(random.random()-0.5, 1) * degreeVertical
    location = (round(cleanerState["LOCATION"][0] + randomHorizon, 1),
                round(cleanerState["LOCATION"][1] + randomVertical, 1))
    cleanerState.update({"LOCATION": location})

def findPath(cleanerState, path):
    pathHorizon = path[0]
    pathVertical = path[1]
    faceHorizon = cleanerState["FACING"][0]
    faceVertical = cleanerState["FACING"][1]
    wholePath = []
    if pathHorizon != 0:
        if faceHorizon*pathHorizon > 0:
            wholePath.append([0, pathHorizon/faceHorizon])
            cleanerState.update({"FACING": (faceHorizon, faceVertical)})
            faceHorizon = faceHorizon
            faceVertical = faceVertical
        elif faceHorizon*pathHorizon < 0:
            wholePath.append([180, -pathHorizon/faceHorizon])
            cleanerState.update({"FACING": (-faceHorizon, faceVertical)})
            faceHorizon = -faceHorizon
            faceVertical = faceVertical

        elif faceHorizon == 0:
            if (pathHorizon > 0) & (faceVertical > 0):
                wholePath.append([90, pathHorizon])
                cleanerState.update({"FACING": (1, 0)})
                faceHorizon = 1
                faceVertical = 0
            if (pathHorizon > 0) & (faceVertical < 0):
                wholePath.append([-90, pathHorizon])
                cleanerState.update({"FACING": (1, 0)})
                faceHorizon = 1
                faceVertical = 0
            if (pathHorizon < 0) & (faceVertical > 0):
                wholePath.append([-90, -pathHorizon])
                cleanerState.update({"FACING": (-1, 0)})
                faceHorizon = -1
                faceVertical = 0
            if (pathHorizon < 0) & (faceVertical < 0):
                wholePath.append([90, -pathHorizon])
                cleanerState.update({"FACING": (-1, 0)})
                faceHorizon = -1
                faceVertical = 0

    if pathVertical != 0:
        if faceVertical*pathVertical > 0:
            wholePath.append([0, pathVertical/faceVertical])
            cleanerState.update({"FACING": (faceHorizon, faceVertical)})
            faceHorizon = faceHorizon
            faceVertical = faceVertical
        elif faceVertical*pathVertical < 0:
            wholePath.append([180, -pathVertical/faceVertical])
            cleanerState.update({"FACING": (faceHorizon, -faceVertical)})
            faceHorizon = faceHorizon
            faceVertical = -faceVertical
        elif faceVertical == 0:
            if (pathVertical > 0) & (faceHorizon > 0):
                wholePath.append([-90, pathVertical])
                cleanerState.update({"FACING": (0, 1)})
                faceHorizon = 0
                faceVertical = 1
            if (pathVertical > 0) & (faceHorizon < 0):
                wholePath.append([90, pathVertical])
                cleanerState.update({"FACING": (0, 1)})
                faceHorizon = 0
                faceVertical = 1
            if (pathVertical < 0) & (faceHorizon > 0):
                wholePath.append([90, -pathVertical])
                cleanerState.update({"FACING": (0, -1)})
                faceHorizon = 0
                faceVertical = -1
            if (pathVertical < 0) & (faceHorizon < 0):
                wholePath.append([-90, -pathVertical])
                cleanerState.update({"FACING": (0, -1)})
                faceHorizon = 0
                faceVertical = -1
    cleanerState.update({"FACING": (faceHorizon, faceVertical)})
    return wholePath

# node status
INITIALNODE = -1
SUCCEEDNODE = 0
RUNNINGNODE = 1
FAILNODE = 2

# super class
class Node:
    parentNode = None
    trueInfo = ""
    falseInfo = ""

    nodeStatus = INITIALNODE

    def __init__(self, trueInfo, falseInfo, parentNode):
        self.trueInfo = trueInfo
        self.falseInfo = falseInfo
        self.parentNode = parentNode
        self.nodeStatus = INITIALNODE

    def setParent(self, parentNode):
        self.parentNode = parentNode

    def evaluateStatus(self):
        return self.nodeStatus

    def run(self, conditions):
        pass



# composite-super class
class Composite(Node):
    childNodes = []

    def __init__(self, trueInfo, falseInfo, parentNode, childNodes):
        self.trueInfo = trueInfo
        self.falseInfo = falseInfo
        self.parentNode = parentNode
        self.childNodes = childNodes
        self.nodeStatus = INITIALNODE

    def addchildNode(self, newNode):
        self.childNodes.append(newNode)

    def setchildNode(self, newNodes):
        self.childNodes = []
        for tempChild in newNodes:
            self.childNodes.append(tempChild)

# composite-sequence
class Sequence(Composite):
    def run(self, conditions):
        self.nodeStatus = RUNNINGNODE
        for tempChild in self.childNodes:
            tempChild.run(conditions)
            tempChildStatus = tempChild.evaluateStatus()
            if tempChildStatus == FAILNODE:
                self.nodeStatus = FAILNODE
                break
        if self.nodeStatus != FAILNODE:
            self.nodeStatus = SUCCEEDNODE
        return True

# composite-selection
class Selection(Composite):
    def run(self, conditions):
        self.nodeStatus = RUNNINGNODE
        for tempChild in self.childNodes:
            tempChild.run(conditions)
            tempChildStatus = tempChild.evaluateStatus()
            if tempChildStatus == SUCCEEDNODE:
                self.nodeStatus = SUCCEEDNODE
                break
        if self.nodeStatus != SUCCEEDNODE:
            self.nodeStatus = FAILNODE
        return True

# composite-priority
class Priority(Composite):
    priorityMap = {}

    def __init__(self, trueInfo, falseInfo, parentNode, childNodes, priorityMap):
        self.trueInfo = trueInfo
        self.falseInfo = falseInfo
        self.parentNode = parentNode
        self.childNodes = childNodes
        self.nodeStatus = INITIALNODE
        self.priorityMap = priorityMap

    def view_priority_map(self):
        print(self.priorityMap)

    def addchildNode(self, newNode, Priority):
        for i in range(len(self.priorityMap) + 1, Priority, -1):
            self.priorityMap.update({i: self.priorityMap[i - 1]})
        self.priorityMap.update({Priority: newNode})
        self.childNodes.append(newNode)

    def run(self, conditions):
        self.nodeStatus = RUNNINGNODE
        for nodeIndex in range(1, len(self.priorityMap) + 1):
            node = self.priorityMap[nodeIndex]
            node.run(conditions)
            indexedNodeStatus = node.evaluateStatus()
            if indexedNodeStatus == SUCCEEDNODE:
                self.nodeStatus = SUCCEEDNODE
                break
        if self.nodeStatus != SUCCEEDNODE:
            self.nodeStatus = FAILNODE
        return True

# decorator-super class
class Decorator(Node):
    childNode = None

    def __init__(self, trueInfo, falseInfo, parentNode, childNode):
        self.trueInfo = trueInfo
        self.falseInfo = falseInfo
        self.parentNode = parentNode
        self.childNode = childNode
        self.nodeStatus = INITIALNODE

    def setchildNode(self, newNode):
        self.childNode = newNode

# decorator-negation
class Negation(Decorator):
    def run(self, conditions):
        self.nodeStatus = RUNNINGNODE
        self.childNode.run(conditions)
        tempStatus = 2 - self.childNode.nodeStatus
        self.nodeStatus = tempStatus
        return True

# decorator-do until succeed/fail
class doUntil(Decorator):
    untilsuccess = False
    untilfail = False

    def __init__(self, trueInfo, falseInfo, parentNode, childNode, untilSuccess):
        self.trueInfo = trueInfo
        self.falseInfo = falseInfo
        self.parentNode = parentNode
        self.childNode = childNode
        self.nodeStatus = INITIALNODE

        if (untilSuccess == True):
            self.untilfail = False
            self.untilsuccess = True

        elif (untilSuccess == False):
            self.untilfail = True
            self.untilsuccess = False

    def run(self, conditions):
        if (self.untilsuccess):
            self.nodeStatus = RUNNINGNODE
            while (True):
                self.childNode.run(conditions)
                tempStatus = self.childNode.evaluateStatus()
                if tempStatus == SUCCEEDNODE:
                    break
            self.nodeStatus = SUCCEEDNODE
            return True
        elif (self.untilfail):
            self.nodeStatus = RUNNINGNODE
            while (True):
                self.childNode.run(conditions)
                tempStatus = self.childNode.evaluateStatus()
                if tempStatus == FAILNODE:
                    break
            self.nodeStatus = SUCCEEDNODE
            return True

# decorator-do according to time
class doTime(Decorator):
    interval = 0

    def __init__(self, trueInfo, falseInfo, parentNode, childNode, interval):
        self.trueInfo = trueInfo
        self.falseInfo = falseInfo
        self.parentNode = parentNode
        self.childNode = childNode
        self.nodeStatus = INITIALNODE
        self.interval = interval

    def run(self, conditions):
        self.nodeStatus = RUNNINGNODE
        tempStatus = 2 - self.childNode.run(conditions, self.interval)
        self.nodeStatus = tempStatus
        return True

# condition-super class
class Condition(Node):
    def check(self, conditions):
        return True

    def run(self, conditions):
        if self.check(conditions) == True:
            self.nodeStatus = SUCCEEDNODE
        else:
            self.nodeStatus = FAILNODE
        return True

# condition-check battery
class checkBattery(Condition):
    def check(self, conditions):
        if conditions["BATTERY_LEVEL"] < 30:
            print("Battery lower than 30.")
            time.sleep(1)
            return True
        else:
            return False

# condition-check spot clean
class checkSpot(Condition):
    def check(self, conditions):
        if conditions["SPOT"] == True:
            print("Start spot clean.")
            time.sleep(1)
            return True
        else:
            return False

# condition-check general clean
class checkGeneral(Condition):
    def check(self, conditions):
        if conditions["GENERAL"] == True:
            print("Start general clean.")
            time.sleep(1)
            return True
        else:
            return False

# condition-check dusty spot
class checkDustySpot(Condition):
    def check(self, conditions):
        if conditions["DUSTY_SPOT"] == True:
            print("Dusty spots exist.")
            time.sleep(1)
            return True
        else:
            return False

# task-super class
class Task(Node):
    def task(self, conditions):
        return True

    def run(self, conditions):
        self.nodeStatus = RUNNINGNODE
        taskStatus = self.task(conditions)
        if (taskStatus):
            self.nodeStatus = SUCCEEDNODE
        elif taskStatus == False:
            self.nodeStatus = FAILNODE
        return True

# task-find path home
class findHome(Task):
    def task(self, conditions):
        conditions.update({"HOME_PATH": findPath(conditions, conditions["LOCATION"])})
        print("Find home now.")
        time.sleep(2)
        return True

# task-go home
class goHome(Task):
    def task(self, conditions):
        print("Go home now.")
        for i in conditions["HOME_PATH"]:
            print("Turn {} degrees.".format(i[0]))
            time.sleep(1)
            print("Go {} meters. ".format(i[1]))
            time.sleep(1)
        conditions.update({"HOME_PATH": []})
        conditions.update({"LOCATION": (0, 0)})
        print("At home now.")
        time.sleep(2)
        return True

# task-dock & charge
class Dock(Task):
    def task(self, conditions):
        print("Dock finished.")
        updateBattery(conditions, 100)
        time.sleep(2)
        print("Start charging.")
        time.sleep(1)
        print("Charge finished.")
        time.sleep(2)
        return True

# task-clean spot
class cleanSpot(Task):
    def task(self, conditions, interval):
        print("Spots at {}".format(conditions["SPOT_LOCATION"]))
        pathHorizon = conditions["SPOT_LOCATION"][0] - conditions["LOCATION"][0]
        pathVertical = conditions["SPOT_LOCATION"][1] - conditions["LOCATION"][1]
        toSpot = findPath(conditions, (pathHorizon, pathVertical))
        for i in toSpot:
            print("Turn {} degrees.".format(i[0]))
            time.sleep(1)
            print("Go {} meters.".format(i[1]))
            time.sleep(1)

        time0 = time.time()
        while (time.time() <= time0 + interval):
            print("Clean spot now, please wait for {} seconds.".format(math.ceil(time0+interval-time.time())))
            time.sleep(1)
            changeLocation(conditions, 1, 1)
            updateBattery(conditions, -1)
        return True

    def run(self, conditions, interval):
        self.nodeStatus = RUNNINGNODE
        taskStatus = self.task(conditions, interval)
        if (taskStatus):
            self.nodeStatus = SUCCEEDNODE
        elif taskStatus == False:
            self.nodeStatus = FAILNODE
        return True

# task-clean dusty spot
class cleanDustySpot(cleanSpot):
    def task(self, conditions, interval):
        print("Spots at {}".format(conditions["DUSTY_SPOT_LOCATION"]))
        pathHorizon = conditions["DUSTY_SPOT_LOCATION"][0] - conditions["LOCATION"][0]
        pathVertical = conditions["DUSTY_SPOT_LOCATION"][1] - conditions["LOCATION"][1]
        toSpot = findPath(conditions, (pathHorizon, pathVertical))
        for i in toSpot:
            print("Turn {} degrees".format(i[0]))
            time.sleep(1)
            print("Go {} meters. ".format(i[1]))
            time.sleep(1)

        time0 = time.time()
        while (time.time() <= time0 + interval):
            print("Clean dusty spot now, please wait for {} seconds.".format(math.ceil(time0+interval-time.time())))
            time.sleep(1)
            changeLocation(conditions, 1, 1)
            updateBattery(conditions, -1)
        return True

# task-done spot
class doneSpot(Task):
    def task(self, conditions):
        print("Spot clean done.")
        conditions.update({"SPOT": False})
        conditions.update({"SPOT_LOCATION": (0, 0)})
        time.sleep(2)
        return True

# task-done dusty spot
class doneDustySpot(Task):
    def task(self, conditions):
        print("Dusty spot done.")
        conditions.update({"DUSTY_SPOT": False})
        conditions.update({"DUSTY_SPOT_LOCATION": (0, 0)})
        time.sleep(2)
        return True

# task-clean
class Clean(Task):
    def task(self, conditions):
        changeLocation(conditions, 2, 2)
        updateBattery(conditions, -10)
        print("Clean floor now.")
        return True

# task-done general
class doneGeneral(Task):
    def task(self, conditions):
        print("Floor clean done.")
        conditions.update({"GENERAL": False})
        time.sleep(2)
        return True

# task-do nothing
class doNothing(Task):
    def task(self, conditions):
        time.sleep(3)
        updateBattery(conditions, -5)
        print("Do nothing.")
        time.sleep(2)
        return True

class Cleaner:
    # priority container
    p1 = Priority("", "", None, [], {})
    # priority 1
    s1 = Sequence("", "", p1, [])
    c1 = checkBattery("", "", s1)
    t1 = findHome("", "", s1)
    t2 = goHome("", "", s1)
    t3 = Dock("", "", s1)
    # priority 1 all child nodes appended
    s1.setchildNode([c1, t1, t2, t3])
    # priority 2
    s2 = Selection("", "", p1, [])
    s2_1 = Sequence("", "", s2, [])
    c2 = checkSpot("", "", s2_1)
    timer_1 = doTime("", "", s2_1, None, 20)
    t4 = cleanSpot("", "", timer_1)
    t5 = doneSpot("", "", s2_1)
    s2_2 = Sequence("", "", s2, [])
    c3 = checkGeneral("", "", s2_2)
    s2_2_1 = Sequence("", "", s2_2, [])
    untilsuc = doUntil("", "", s2_2_1, [], untilSuccess=True)
    s2_2_1_1 = Sequence("", "", s2_2_1, [])
    n1 = Negation("", "", s2_2_1_1, [])
    c4 = checkBattery("", "", n1)
    s2_2_1_1_1 = Selection("", "", s2_2_1_1, [])
    s2_2_1_1_1_1 = Sequence("", "", s2_2_1_1_1, [])
    c5 = checkDustySpot("", "", s2_2_1_1_1_1)
    timer_2 = doTime("", "", s2_2_1_1_1_1, None, 35)
    t6 = cleanDustySpot("", "", timer_2)
    t10 = doneDustySpot("", "", timer_2)
    t7 = Clean("", "", s2_2_1_1_1)
    t8 = doneGeneral("", "", s2_2_1)
    # priority 2 all child nodes appended
    s2.setchildNode([s2_1, s2_2])
    s2_1.setchildNode([c2, timer_1, t5])
    timer_1.setchildNode(t4)
    s2_2.setchildNode([c3, s2_2_1])
    s2_2_1.setchildNode([untilsuc, t8])
    untilsuc.setchildNode(s2_2_1_1)
    s2_2_1_1.setchildNode([n1, s2_2_1_1_1])
    n1.setchildNode(c4)
    s2_2_1_1_1.setchildNode([s2_2_1_1_1_1, t7])
    s2_2_1_1_1_1.setchildNode([c5, timer_2, t10])
    timer_2.setchildNode(t6)
    # priority 3
    t9 = doNothing("", "", p1)
    # append tasks to corresponding parent node
    p1.addchildNode(s1, 1)
    p1.addchildNode(s2, 2)
    p1.addchildNode(t9, 3)



    def run(self, cleanrState):
        while (True):
            rand = random.random()
            if rand > 0.75:
                cleanrState.update({"SPOT": True})
                cleanrState.update({"SPOT_LOCATION": (round(random.random() * 10, 1), round(random.random() * 10, 1))})
                cleanrState.update({"GENERAL": False})
                print("--------------------------------------------------")
                print("Spot clean activated, general clean not activated.")
                print("--------------------------------------------------")
            elif rand >0.5:
                cleanrState.update({"SPOT": False})
                print("--------------------------------------------------")
                print("Spot clean not activated, general clean activated.")
                cleanrState.update({"GENERAL": True})
                if rand > 0.375:
                    cleanrState.update({"DUSTY_SPOT": True})
                    print("Dusty spots exist and dusty spot clean will be activated.")
                    print("---------------------------------------------------------")
                    cleanrState.update({"DUSTY_SPOT_LOCATION": (
                    round(random.random() * 100, 1), round(random.random() * 100, 1))})
                else:
                    cleanrState.update({"DUSTY_SPOT": False})
                    print("Dusty spots not exist and dusty spot clean will not be activated.")
                    print("-----------------------------------------------------------------")
            elif rand > 0.25:
                cleanrState.update({"SPOT": True})
                print("--------------------------------------------------")
                print("Spot clean activated, general clean activated.")
                cleanrState.update({"SPOT_LOCATION": (round(random.random() * 10, 1), round(random.random() * 10, 1))})
                cleanrState.update({"GENERAL": True})
                if rand > 0.125:
                    cleanrState.update({"DUSTY_SPOT": True})
                    print("Dusty spots exist and dusty spot clean will be activated.")
                    print("---------------------------------------------------------")
                    cleanrState.update({"DUSTY_SPOT_LOCATION": (
                        round(random.random() * 100, 1), round(random.random() * 100, 1))})
                else:
                    cleanrState.update({"DUSTY_SPOT": False})
                    print("Dusty spots not exist and dusty spot clean will not be activated.")
                    print("-----------------------------------------------------------------")
            else:
                cleanrState.update({"SPOT":False})
                cleanrState.update({"GENERAL":False})
                print("--------------------------------------------------")
                print("Spot clean not activated, general clean not activated.")
                print("--------------------------------------------------")
            print("Battery: " + str(cleanrState["BATTERY_LEVEL"]))
            self.p1.run(cleanrState)

if __name__=="__main__":
    myCleaner=Cleaner()
    myCleaner.run(cleanerState)

