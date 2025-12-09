import cv2
import mediapipe as mp
import joblib
from func import normalize_point, predict_gesture

def good():

    model_filename = 'svm_hand_model.pkl'
    model = joblib.load(model_filename)
    print("모델 로드 완료!")


    mp_drawing=mp.solutions.drawing_utils
    mp_drawing_style=mp.solutions.drawing_styles

    #pose시
    mp_pose=mp.solutions.pose

    #hands 시
    mp_hands = mp.solutions.hands



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
            if cv2.waitKey(1) & 0xFF == ord('0'):
              target_label = 0

              print('------'*10)
            if target_label != -1:
                n_data = normalize_point(hand_landmarks)
                print("전처리 성공")

                result, conf ,poss = predict_gesture(n_data,model)

                print(f"가위(0): {poss[0][0] * 100:.1f}%")
                print(f"바위(1): {poss[0][1] * 100:.1f}%")
                print(f"보  (2): {poss[0][2] * 100:.1f}%")
                print("-" * 20)

                # 로봇이 확실할때만 움직이라고 설정 <- 안정성때문에
                if conf > 0.8:
                    if result == 0:
                        print("Final_Result: 가위")
                        return result
                    elif result == 1:
                        print("Final_Result: 바위")
                        return result
                    elif result == 2:
                        print("Final_Result: 보")
                        return result




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

good()