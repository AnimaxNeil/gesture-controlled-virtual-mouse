import numpy
import VideoCaptureModule as VCM
import HandsDetectionModule as HDM
import UIControlModule as UICM
import IOModule as IOM


class VirtualMouse:

    paddingX=400
    paddingY=200
    overflowX=100
    overflowY=100
    edgeAdjustX=30
    edgeAdjustY=20

    def __init__(self):
        self.uiControler = UICM.UIControl()
        self.handsDetector = HDM.HandsDetection(maxHands=1)
        self.videoCapture = VCM.VideoCapture(
            camIndex=0,
            windowName="Hand Tracking Window")
        
    def set(self, paddingX=None, paddingY=None,
             overflowX=None, overflowY=None, edgeAdjustX=None, edgeAdjustY=None):
        if paddingX: self.paddingX = paddingX
        if paddingY: self.paddingY = paddingY
        if overflowX: self.overflowX = overflowX
        if overflowY: self.overflowY = overflowY
        if edgeAdjustX: self.edgeAdjustX = edgeAdjustX
        if edgeAdjustY: self.edgeAdjustY = edgeAdjustY
        
    def handsTracking(self, img):
        handsPositions, img = self.handsDetector.findHands(img)
        if handsPositions and len(handsPositions) > 0:
            handPos = handsPositions[0]
            if handPos and len(handPos) == 21:
                self.checkMouseMovement(handPos)
                self.checkLeftClick(handPos)
                self.checkRightClick(handPos)
        return img

    def start(self):
        self.videoCapture.set(
            paddingX=400,
            paddingY=200,
            overflowX=100,
            overflowY=100,
            flip=True,
            showFps=True,
            exitOnEsc=True)
        self.videoCapture.startCaptureLoop(runFunction=self.handsTracking)

    def imgToScreenCoordinates(self, handPos, relaxed=False):
        mx, my = handPos[HDM.FingerUtility.getTipIndex(HDM.FingerUtility.Finger.INDEX)]
        if not self.videoCapture.checkIfCoordinatesInTrackPad(mx, my, relaxed):
            return -1, -1
        sx = numpy.interp(mx, (self.videoCapture.trackPadMinX + self.edgeAdjustX,
                self.videoCapture.trackPadMaxX - self.edgeAdjustX),
                (self.uiControler.screenWidth, 0))
        sy = numpy.interp(my, (self.videoCapture.trackPadMinY + self.edgeAdjustY,
                self.videoCapture.trackPadMaxY - self.edgeAdjustY),
                           (0, self.uiControler.screenHeight))
        return int(sx), int(sy)

    def checkMouseMovement(self, handPos):
        sx, sy = self.imgToScreenCoordinates(handPos)
        if (sx > -1 and sy > -1 and
            HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.INDEX) and
            not HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.RING) and
            not HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.PINKY)):
            IOM.printToConsole((sx, sy), False)
            self.uiControler.moveCursor(sx, sy)

    def checkLeftClick(self, handPos):
        sx, sy = self.imgToScreenCoordinates(handPos, True)
        if (sx > -1 and sy > -1 and 
            HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.INDEX) and
            not HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.RING) and
            not HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.PINKY) and
            HDM.FingerUtility.checkFingerPointsTouching(handPos, 
            HDM.FingerUtility.getTipIndex(HDM.FingerUtility.Finger.THUMB),
            HDM.FingerUtility.getMidIndex(HDM.FingerUtility.Finger.INDEX))):
            IOM.printToConsole("<--", False)
            self.uiControler.handleLeftClick()

    def checkRightClick(self, handPos):
        sx, sy = self.imgToScreenCoordinates(handPos, True)
        # if (sx > -1 and sy > -1 and
        #     HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.INDEX) and
        #     HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.MIDDLE) and
        #     not HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.RING) and
        #     not HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.PINKY) and
        #     HDM.FingerUtility.checkFingerPointsTouching(handPos, 
        #     HDM.FingerUtility.getTipIndex(HDM.FingerUtility.Finger.MIDDLE),
        #     HDM.FingerUtility.getTipIndex(HDM.FingerUtility.Finger.INDEX))):
        if (sx > -1 and sy > -1 and
            HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.INDEX) and
            not HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.RING) and
            HDM.FingerUtility.checkFingerUp(handPos, HDM.FingerUtility.Finger.PINKY) and
            HDM.FingerUtility.checkFingerPointsTouching(handPos, 
            HDM.FingerUtility.getTipIndex(HDM.FingerUtility.Finger.THUMB),
            HDM.FingerUtility.getMidIndex(HDM.FingerUtility.Finger.INDEX))):
            IOM.printToConsole("-->", False)
            self.uiControler.rightClick()


def main():
    IOM.printToConsole("Virtual Mouse Started")
    virtualMouse = VirtualMouse()
    virtualMouse.start()


if __name__ == "__main__":
    main()

