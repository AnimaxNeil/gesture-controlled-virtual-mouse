import pyautogui


class UIControl:

    preX, preY = 0, 0
    nowX, nowY = 0, 0
    smoothening = 0.3

    def __init__(self):
        self.screenWidth, self.screenHeight = pyautogui.size()
        pyautogui.FAILSAFE = False

    def moveCursor(self, x, y):
        self.nowX = self.preX + (x - self.preX) * self.smoothening
        self.nowY = self.preY + (y - self.preY) * self.smoothening
        pyautogui.moveTo(self.nowX, self.nowY)
        self.preX, self.preY = self.nowX, self.nowY
    
    def leftClick(self):
        pyautogui.leftClick()

    def rightClick(self):
        pyautogui.rightClick()