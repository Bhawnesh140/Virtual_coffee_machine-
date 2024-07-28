import os
from cvzone.HandTrackingModule import HandDetector
import cv2

# Initialize webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 1000)  # Set width
cap.set(4, 480)   # Set height

# Load background image
imgBackground = cv2.imread("Interface/Background.png")

# Import all mode images to the list
folderPathModes = "Interface/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = [cv2.imread(os.path.join(folderPathModes, imgModePath)) for imgModePath in listImgModesPath]

# Import all icons to the list
folderPathIcons = "Interface/Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = [cv2.imread(os.path.join(folderPathIcons, imgIconsPath)) for imgIconsPath in listImgIconsPath]

# Initialize variables
modeType = 0  # for changing selection mode
selection = -1
counter = 0
selectionspeed = 12
detector = HandDetector(maxHands=1, detectionCon=0.5)
modepostions = [(1136, 196), (1000, 384), (1136, 581)]
counterpause = 0
selectionlist = [-1, -1, -1]

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    hands, img = detector.findHands(img, draw=True, flipType=True)

    # Resize the webcam feed
    img = cv2.resize(img, (561, 440))  # Resize to 600x450

    # Overlaying the resized webcam feed on the background image
    imgBackground[145:145 + 440, 739:739 + 561] = img

    # Resize the mode image to fit the designated area
    imgModeResized = cv2.resize(listImgModes[modeType], (433, 720))
    imgBackground[0:720, 0:433] = imgModeResized

    if hands and counterpause == 0 and modeType < 3:
        # Information for the first hand detected
        hand1 = hands[0]  # Get the first hand detected

        # Count the number of fingers up for the first hand
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
                selection = 1

        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
                selection = 2

        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
                selection = 3

        else:
            selection = -1
            counter = 0

        if counter > 0:
            counter += 1
            print(counter)
            cv2.ellipse(imgBackground, modepostions[selection - 1], (103, 103), 0, 0, counter * selectionspeed, (0, 255, 0), 20)

        if counter * selectionspeed > 360:
            selectionlist[modeType] = selection
            modeType += 1
            counter = 0
            selection = -1
            counterpause = 1

    # Pause after each selection is made
    if counterpause > 0:
        counterpause += 1
        if counterpause > 60:  # Because frame rate is 30 per sec
            counterpause = 0

    # Add selection icons at the bottom
    if selectionlist[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionlist[0] - 1]
    if selectionlist[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionlist[1]]
    if selectionlist[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionlist[2]]

    # Display the image
    cv2.imshow("Background", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


#kvdsbvdbvdb
 # Add selection icons at the bottom
    if selectionlist[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionlist[0] - 1]
    if selectionlist[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionlist[1]]
    if selectionlist[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionlist[2]]
