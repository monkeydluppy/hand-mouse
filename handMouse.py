import cv2
import mediapipe as mp
import pyautogui
import numpy as np


pyautogui.FAILSAFE = False

# code to capture video and initialise hand deteting utilities
capture = cv2.VideoCapture(0)
mp_detect_hand = mp.solutions.hands
hands = mp_detect_hand.Hands()
mp_drawing = mp.solutions.drawing_utils

frameR = 100  # frame reduction

while True:
    # capture the frame from camera and detect hands
    ign, frame = capture.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_output = hands.process(rgb_frame)

    frame_height, frame_width, ign = frame.shape

    screen_width, screen_height = pyautogui.size()

    # draw all the landmarks and connections on detected hands
    if hand_output.multi_hand_landmarks:
        for hand in hand_output.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand, mp_detect_hand.HAND_CONNECTIONS)

            landmarks = hand.landmark

            # store xand y, cordinates of each landmarks
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)

                # draw rectangle indiacting that youll limit the screen whintin that range
                cv2.rectangle(frame, (frameR, frameR), (frame_width -
                              frameR, frame_height-frameR - 100), (255, 0, 255), 2)

                # draw circle and store x,y co ordinates of lanmark 0
                if id == 0:
                    cv2.circle(img=frame, center=(x, y),
                               radius=15, color=(255, 0, 255))
                    main_x = int(screen_width/frame_width)*x
                    main_y = int(screen_height/frame_height)*y

                if id == 8:
                    ind_x = x
                    ind_y = y
                    cv2.circle(frame, (x, y),
                               15, (255, 0, 255))
                    index_x = int(screen_width/frame_width)*x
                    index_y = int(screen_height/frame_height)*y

                if id == 12:
                    cv2.circle(frame, (x, y),
                               15, (255, 0, 255))
                    ring_x = int(screen_width/frame_width)*x
                    ring_y = int(screen_height/frame_height)*y

                    # if index and ring finger is up, go to clicking mode
                    if ((main_y - ring_y) > 200):
                        print(main_y, main_y - ring_y, ring_y)
                        if (-90 < (ring_x - index_x) < 0):
                            print(ring_x - index_x, "click")
                            pyautogui.click()

                    # else to moving mode
                    else:
                        # limit the screen within the range of that previously drawn rectangle
                        cv2.circle(frame, (ind_x, ind_y),
                                   15, (255, 0, 255), cv2.FILLED)
                        move_x = np.interp(
                            ind_x, (frameR, frame_width - frameR), (0, screen_width))
                        move_y = np.interp(
                            ind_y, (frameR, frame_height - frameR - 100), (0, screen_height))
                        pyautogui.moveTo(move_x, move_y)
                        print(move_x, move_y)
    # function to launch camera and show captured frame
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
