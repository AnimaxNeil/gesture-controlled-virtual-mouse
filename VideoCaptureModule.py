import cv2
import time


class VideoCapture:

    def __init__(self, camIndex = 0, windowName = "Video Capture Window", windowWidth=640, windowHeight=480):
        self.camIndex = camIndex
        self.windowName = windowName
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.cap = cv2.VideoCapture(camIndex)
        self.pTime = self.cTime = 0

    def startCaptureLoop(self, runFunction, paddingX=10, paddingY=10,
                         overflowX=0, overflowY=10, flip=False, showFps=True, exitOnEsc=True):
        self.paddingX = paddingX
        self.paddingY = paddingY
        self.overflowX = overflowX
        self.overflowY = overflowY
        self.flip = flip
        self.showFps = showFps
        self.exitOnEsc = exitOnEsc
        pTime = 0
        cTime = 0
        while self.cap.isOpened():
            success, img = self.cap.read()
            if not success:
                break
            img.flags.writeable = False
            # cv2.resize(img, (self.windowWidth, self.windowHeight))
            if runFunction:
                runFunction(img)
            self.imgHeight, self.imgWidth, self.imgChannels = img.shape
            self.trackPadMinX = int(self.paddingX)
            self.trackPadMaxX = int(self.imgWidth - self.paddingX)
            self.trackPadMinY = int(self.paddingY / 1.5)
            self.trackPadMaxY = int(self.imgHeight - self.paddingY * 1.5)
            cv2.rectangle(img, (self.trackPadMinX, self.trackPadMinY), 
                          (self.trackPadMaxX, self.trackPadMaxY), (255,0,255), 2)
            if self.flip:
                img = cv2.flip(img, 1)
            if self.showFps:
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            # cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
            cv2.imshow(self.windowName, img)
            # cv2.resizeWindow(self.windowName, self.windowWidth, self.windowHeight)
            key = cv2.waitKey(1)
            if cv2.getWindowProperty(self.windowName, cv2.WND_PROP_VISIBLE) < 1:
                break
            if self.exitOnEsc and key == 27:
                break
        cv2.destroyAllWindows()

    def checkIfCoordinatesInTrackPad(self, mx, my, relaxed=False):
        if not relaxed:
            return (mx > self.trackPadMinX and mx < self.trackPadMaxX and
                    my > self.trackPadMinY and my < self.trackPadMaxY)
        return (mx > self.trackPadMinX - self.overflowX and mx < self.trackPadMaxX + self.overflowX and
            my > self.trackPadMinY - self.overflowY and my < self.trackPadMaxY + self.overflowY)

    @staticmethod
    def img_BGRtoRGB(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
