import enum
import mediapipe
import IOModule as IOM


class FingerUtility:

    class Finger(enum.Enum):
        THUMB = 1
        INDEX = 2
        MIDDLE = 3
        RING = 4
        PINKY = 5

    upThresholdMin = 10
    touchThresholdMax = 20

    @staticmethod
    def set(upThresholdMin=None, touchThresholdMax=None):
        FingerUtility.upThresholdMin = upThresholdMin
        FingerUtility.touchThresholdMax = touchThresholdMax

    @staticmethod
    def getTipIndex(finger):
        return finger.value * 4
    
    @staticmethod
    def getPreTipIndex(finger):
        return FingerUtility.getTipIndex(finger) - 1
    
    @staticmethod
    def getMidIndex(finger):
        return FingerUtility.getTipIndex(finger) - 2
    
    @staticmethod
    def checkFingerUp(handPos, finger):
        tx, ty = handPos[FingerUtility.getTipIndex(finger)]
        mx, my = handPos[FingerUtility.getMidIndex(finger)]
        distanceY = my - ty
        IOM.printToConsole(distanceY, False)
        return distanceY > FingerUtility.upThresholdMin
    
    @staticmethod
    def findSquareDistance(handPos, fingerPoint1, fingerPoint2):
        x1, y1 = handPos[fingerPoint1]
        x2, y2 = handPos[fingerPoint2]
        return pow(pow(x2 - x1, 2) + pow(y2 - y1, 2), 0.5)
    
    @staticmethod
    def checkFingerPointsTouching(handPos, fingerPoint1, fingerPoint2):
        distance = FingerUtility.findSquareDistance(handPos, fingerPoint1, fingerPoint2)
        IOM.printToConsole(distance, False)
        return distance < FingerUtility.touchThresholdMax


class HandsDetection:

    def __init__(self, imgMode=False, maxHands=2, detectionConfidence=0.5, trackingConfidence=0.5):
        self.imgMode = imgMode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackingConfidence = trackingConfidence
        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode = self.imgMode,
            max_num_hands = self.maxHands,
            min_detection_confidence = self.detectionConfidence,
            min_tracking_confidence = self.trackingConfidence)
        self.mpDraw = mediapipe.solutions.drawing_utils

    def findHands(self, img, draw=True):
        results = self.hands.process(img)
        handsPositions = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                handPos = []
                for id, lm in enumerate(handLms.landmark):
                    imgHeight, imgWidth, imgChannels = img.shape
                    cx, cy = int(lm.x * imgWidth), int(lm.y * imgHeight)
                    handPos.append((cx, cy))
                handsPositions.append(handPos)
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return handsPositions, img
