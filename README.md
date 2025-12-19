# 🖐️ Hand Gesture Controlled Dual Robot Arms (Python & ROS 2)

이 프로젝트는 웹캠을 통해 손 제스처(가위, 바위, 보)를 인식하고, 인식된 결과에 따라 **두 대의 Universal Robot(UR)**을 동시에 제어하는 시스템입니다.

사용자의 환경에 따라 두 가지 실행 방식을 지원합니다:

1. **Standalone Mode:** 파이썬 스크립트 하나로 실행 (간편함)
2. **ROS 2 Mode:** 노드 간 통신(Topic)을 이용한 분산 제어 (확장성 높음)

---

## 📋 주요 기능 (Features)

* **실시간 손 인식:** MediaPipe Hands를 이용한 빠르고 정확한 손 랜드마크 추출
* **듀얼 로봇 제어:** 하나의 제스처 입력으로 두 대의 로봇(Robot 1, Robot 2)을 동시에 제어
* **ROS 2 지원:** Publisher(Vision)와 Subscriber(Control) 노드 분리 구조 지원
* **데이터 정규화:** 손의 거리나 위치에 상관없이 인식되도록 좌표 정규화 알고리즘(`func.py`) 적용
* **안전 장치:** 예측 정확도(Confidence)가 80% 이상일 때만 로봇 동작 명령 전송

---

## 🛠️ 기술 스택 (Tech Stack)

* **Language:** Python 3.x
* **Framework:** ROS 2 (Humble 권장)
* **Computer Vision:** OpenCV, MediaPipe
* **Machine Learning:** Scikit-learn (SVM), Joblib, Pandas
* **Robot Communication:** TCP/IP Socket (UR Script)

---

## 📂 파일 구조 (File Structure)

### 🔹 공통 / 학습 관련 (Common)

| 파일명 | 설명 |
| :--- | :--- |
| `point_to_csv.py` | 학습 데이터 수집용 스크립트 (웹캠 + 키보드 입력) |
| `model_train.py` | 수집된 `hand_data.csv`를 학습시켜 `svm_hand_model.pkl` 모델 생성 |
| `func.py` | 좌표 정규화 및 예측 유틸리티 함수 |
| `no_wait.py` | 로봇 소켓 통신 모듈 (IP 전송 및 제어) |

<br>

### 🔹 모드 1: Standalone Python

| 파일명 | 설명 |
| :--- | :--- |
| `prediction_result.py` | **[메인]** 비전 인식과 로봇 제어를 하나의 파일에서 실행 |
| `prediction_result_real.py` | 로봇 연결 없이 인식 결과만 테스트하는 파일 |

<br>

### 🔹 모드 2: ROS 2 (New)

| 파일명 | 설명 |
| :--- | :--- |
| `prediction_result_ros.py` | **[Publisher Node]** 웹캠으로 손을 인식하고 결과(0, 1, 2)를 Topic으로 발행 |
| `control_ros.py` | **[Subscriber Node]** Topic을 수신하고 `no_wait.py`를 호출하여 로봇 제어 |

---

## 🚀 설치 및 학습 (Common Setup)

### 1. 라이브러리 설치

```bash
pip install opencv-python mediapipe scikit-learn pandas joblib numpy
# ROS 2 환경의 경우 rclpy는 ROS 설치 시 기본 포함되어 있습니다.
```

### 2. 데이터 수집 및 학습

```bash
# 1. 데이터 수집 (0:가위, 1:바위, 2:보)
python point_to_csv.py

# 2. 모델 학습 (svm_hand_model.pkl 생성)
python model_train.py
```

---

## 🎮 실행 방법 1: Standalone Mode (Python Only)

ROS 설치 없이 간단하게 실행하고 싶을 때 사용합니다.

1. **로봇 IP 설정:** `prediction_result.py` 파일 내 `ip_1`, `ip_2` 수정
2. **실행:**

```bash
python prediction_result.py
```

---

## 🤖 실행 방법 2: ROS 2 Mode

기능별로 노드를 나누어 실행합니다. (ROS 2 패키지 빌드 필요)

### 1. 패키지 구성 및 빌드

작성된 파일들을 ROS 2 패키지 디렉토리(`~/ros2_ws/src/패키지명/패키지명/`)에 위치시키고 빌드합니다.

### 2. 실행

터미널을 2개 열어 각각 실행합니다.

**Terminal 1: 로봇 제어 노드 (Subscriber)**

```bash
# 로봇 제어 노드 실행
ros2 run <패키지명> control_ros
```

**Terminal 2: 비전 인식 노드 (Publisher)**

```bash
# 웹캠이 켜지고 제스처 인식 시작
ros2 run <패키지명> prediction_result_ros
```

### 3. 통신 구조

* **Topic Name:** `/gesture_result`
* **Message Type:** `std_msgs/Int32`
* **Flow:** `[Vision Node] --(Int32)--> [Control Node] --(Socket)--> [UR Robots]`

---

## 📊 로봇 동작 매핑 (Coordinates)

각 제스처 인식 시 두 로봇은 협동 동작을 수행합니다.

| 제스처 | Robot 1 (ip_1) | Robot 2 (ip_2) |
| :--- | :--- | :--- |
| **가위 (0)** | `[-40.96, -86.11, ...]` | `[50.78, -97.04, ...]` |
| **바위 (1)** | `[-43.20, -66.50, ...]` | `[40.75, -136.46, ...]` |
| **보 (2)** | `[-136.76, -62.32, ...]` | `(설정된 좌표)` |

---

## ⚠️ 안전 주의사항 (Safety Warning)

1. **동시 동작 주의:** 두 대의 로봇이 동시에 움직이므로 작업 반경이 겹치지 않는지 확인하세요.
2. **ROS 지연:** 무선 네트워크 사용 시 토픽 발행과 로봇 동작 사이에 약간의 지연이 발생할 수 있습니다.
3. **비상 정지:** 테스트 시 반드시 E-Stop 버튼을 확보하세요.
