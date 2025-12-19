import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32  # 숫자(0, 1, 2)를 보내기 위함
import cv2
import mediapipe as mp
import joblib
import numpy as np
from hand_gesture_control.func import normalize_point, predict_gesture # 경로 주의

class GesturePublisher(Node):
    def __init__(self):
        super().__init__('gesture_publisher')
        self.publisher_ = self.create_publisher(Int32, 'gesture_result', 10)
        self.timer = self.create_timer(0.1, self.timer_callback) # 0.1초마다 실행

        # 모델 로드 및 MediaPipe 설정
        self.model = joblib.load('/path/to/your/svm_hand_model.pkl') # 절대 경로 권장
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5)
        self.cap = cv2.VideoCapture(0)
        self.get_logger().info("Vision Node Started")

    def timer_callback(self):
        success, image = self.cap.read()
        if not success:
            return

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                n_data = normalize_point(hand_landmarks)
                result, conf, _ = predict_gesture(n_data, self.model)

                # 정확도가 80% 이상일 때만 토픽 발행
                if conf > 0.8:
                    msg = Int32()
                    msg.data = int(result)
                    self.publisher_.publish(msg)
                    self.get_logger().info(f'Published Gesture: {result}')

        # 화면 출력 (선택 사항)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow('Hand Gesture', image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = GesturePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()