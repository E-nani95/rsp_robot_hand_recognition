import cv2
import mediapipe as mp
import math
import os
import csv
from func import normalize_point

mp_drawing=mp.solutions.drawing_utils
mp_drawing_style=mp.solutions.drawing_styles
#pose시
mp_pose=mp.solutions.pose

#hands 시
mp_hands = mp.solutions.hands


file_name = 'hand_data.csv'

# 파일이 없으면 헤더(제목줄)를 먼저 씁니다. 컬럼을
if not os.path.exists(file_name):
    with open(file_name, mode='w', newline='') as f:
        writer = csv.writer(f)
        header = ['label']
        for i in range(21):
            header.extend([f'x{i}', f'y{i}'])
        writer.writerow(header)

#hand
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    image_height, image_width, _ = image.shape
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        target_label=-1
        check_num_0=0
        check_num_1=0
        check_num_2=0
        if cv2.waitKey(1) & 0xFF == ord('0'):
          target_label = 0
          check_num_0 += 1
        elif cv2.waitKey(1) & 0xFF == ord('1'):
          target_label = 1
          check_num_1 += 1
        elif cv2.waitKey(1) & 0xFF == ord('2'):
          target_label = 2
          check_num_2 += 1

          print('------'*10)
        if target_label != -1:
          n_data = normalize_point(hand_landmarks)

          print("---------------------------------------")

          n_data = [target_label] + n_data

          with open(file_name,mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(n_data)
        if target_label==0:
          print(f"데이터 저장됨: Label 가위, 갯수: {check_num_0}")
        elif target_label == 1:
          print(f"데이터 저장됨: Label 바위, 갯수: {check_num_1}")
        elif target_label ==2:
          print(f"데이터 저장됨: Label 보, 갯수: {check_num_2}")


        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_style.get_default_hand_landmarks_style(),
            mp_drawing_style.get_default_hand_connections_style()
        )
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()