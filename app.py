import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)


class DragImg():
    def __init__(self, path, posOrigin, imgType):
        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]  # (height, width)

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size

        # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2


# Load all images in folder
path = "ImagesPNG"
myList = os.listdir(path)
print(myList)

listImg = []
for x, pathImg in enumerate(myList):
    if 'png' in pathImg.lower():
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}', [50 + x * 300, 50], imgType))

# Main loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        # Use only x, y (2D) positions
        point1 = lmList[8][:2]
        point2 = lmList[12][:2]
        length, info, img = detector.findDistance(point1, point2, img)

        if length < 60:
            cursor = point1
            for imgObject in listImg:
                imgObject.update(cursor)

    try:
        for imgObject in listImg:
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img
    except Exception as e:
        print("Error drawing images:", e)

    cv2.imshow("Drag and Drop", img)
    cv2.waitKey(1)

