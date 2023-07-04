import pyautogui
import time
import IOModule as IOM


class UIControl:

    cursorSmoothening = 0.3
    clickIntervalWait = 0.5
    dragClickThreshold = 1
    preX = preY = nowX = nowY = 0
    preLeftClickTime = nowLeftClickTime = leftClickTimer = 0

    def __init__(self):
        self.screenWidth, self.screenHeight = pyautogui.size()
        pyautogui.FAILSAFE = False

    def set(self, cursorSmoothening=None, clickIntervalWait=None, dragClickThreshold=None):
        if cursorSmoothening: self.cursorSmoothening = cursorSmoothening
        if clickIntervalWait: self.clickIntervalWait = clickIntervalWait
        if dragClickThreshold: self.dragClickThreshold = dragClickThreshold

    def moveCursor(self, x, y):
        self.nowX += (x - self.preX) * self.cursorSmoothening
        self.nowY += (y - self.preY) * self.cursorSmoothening
        pyautogui.moveTo(self.nowX, self.nowY)
        self.preX, self.preY = self.nowX, self.nowY

    def handleLeftClick(self):
        self.preLeftClickTime = self.nowLeftClickTime
        if self.preLeftClickTime == 0:
            self.leftClickTimer= 0
            self.preLeftClickTime = time.time()
        self.nowLeftClickTime = time.time()
        self.leftClickTimer += self.nowLeftClickTime - self.preLeftClickTime
        IOM.printToConsole(self.leftClickTimer, False)
        if self.nowLeftClickTime - self.preLeftClickTime > self.clickIntervalWait:
            self.leftClickTimer = 0
            IOM.printToConsole("Click", False)
            self.leftClick()
            return
        if self.leftClickTimer > self.dragClickThreshold:
            IOM.printToConsole("Drag", False)
            self.leftClickDragStart()
    
    def leftClick(self):
        self.leftClickDragStop()
        pyautogui.leftClick()

    def rightClick(self):
        self.leftClickDragStop()
        pyautogui.rightClick()

    def leftClickDragStart(self):
        pyautogui.mouseDown()

    def leftClickDragStop(self):
        pyautogui.mouseUp()

