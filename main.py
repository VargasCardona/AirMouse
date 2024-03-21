import cv2
import mediapipe as mp
import numpy as np
from math import *
import threading
import pyautogui

mp_drawing = mp.solutions.drawing_utils # Drawing depencencies
mp_hands = mp.solutions.hands # Mediapipe's pre-trained hand tracking model

#Work Boundaries
work_area = 115
coords = (0,0)
is_moving_enabled = True

# Setting up viewport
cam_width, cam_height = 640, 480
cap = cv2.VideoCapture(1)
cap.set(3, cam_width)
cap.set(4, cam_height)

# Measure the distance between two coodinates
def measure_distance(coord_x1, coord_y1, coord_x2, coord_y2):
    return ceil(sqrt(pow(coord_x1-coord_x2, 2)+pow(coord_y1-coord_y2, 2)))

# Movement Thread
def move_mouse():
    global coords
    global resolution
    global is_moving_enabled

    screen_width, screen_height = pyautogui.size() # Screen size

    mapped_coords = (np.interp(coords[0], (work_area, cam_width - work_area), (0, screen_width)),
                    np.interp(coords[1], (work_area, cam_height - work_area), (0, screen_height))) # Scaled coordinates
    if is_moving_enabled:
       pyautogui.moveTo(mapped_coords[0], mapped_coords[1], duration=0.1) # Move the pointer with a 0.1 delay

# Detection
with mp_hands.Hands(
 static_image_mode=False,
 max_num_hands=1,
 min_detection_confidence=0.5) as hands:

# Detection loop
 while True:
  _, image = cap.read()
  
  image = cv2.flip(image, 1)
  threading.Thread(target = move_mouse).start()
  height, width, _ = image.shape
  resolution = (image.shape[1], image.shape[0])
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  results = hands.process(image_rgb)
  
  if results.multi_hand_landmarks is not None: # Creating Landmarks
    for hand_landmarks in results.multi_hand_landmarks: # Draw a landmark for each detection
       index_coords = (int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width), # Location for Index Finger
                      int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height))

       middle_coords = (int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width), # Location for Middle Finger
                       int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height))

       wrist_coords = (int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * cam_width), # Locaton for Wrist Landmark
                      int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * cam_height)) 

       recog_boundaries = measure_distance(index_coords[0], index_coords[1], wrist_coords[0], wrist_coords[1]) # Boundaries for work area

       if 240 > recog_boundaries > 180: # Minumum distance for detection

                # Make landmarks visible
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, # 
                mp_drawing.DrawingSpec(color=(0,0,255),thickness=-1, circle_radius=5), # Draw circles in each joint
                mp_drawing.DrawingSpec(color=(0,40,255),thickness=2,)) # Connect each landmark

                coords = (index_coords[0], index_coords[1])
    
                cv2.rectangle(image, (work_area, work_area), (cam_width - work_area, cam_height - work_area), (0, 0, 255), 1) # Rendering work area

                if measure_distance(middle_coords[0], middle_coords[1], wrist_coords[0], wrist_coords[1]) > 120: # Checking if index finger present
                   is_moving_enabled = False

                   if measure_distance(index_coords[0], index_coords[1], middle_coords[0], middle_coords[1]) < 30: # Measure distance for click
                      cv2.circle(image, (index_coords[0],index_coords[1]), 5, (0,255,255), 2)
                      pyautogui.click()
                else:
                   is_moving_enabled = True # Enables movement

        
  cv2.imshow("image", image) # Displays viewport
  if cv2.waitKey(20) & 0xFF==ord('d'): # Kill the main thread if the "d" key is pressed
     break
    
cap.release() # Releases the input method
cv2.destroyAllWindows() # Deletes the viewport
