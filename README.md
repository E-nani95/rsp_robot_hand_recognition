# 🖐️ Hand Gesture Controlled Robot Arm (UR Robot)

이 프로젝트는 웹캠을 통해 손 제스처(가위, 바위, 보)를 인식하고, 인식된 결과에 따라 Universal Robot(UR) 로봇 팔을 제어하는 시스템입니다.

Google의 **MediaPipe**를 사용하여 손의 랜드마크를 추출하고, **SVM(Support Vector Machine)** 모델을 통해 제스처를 분류하며, **TCP/IP 소켓 통신**을 통해 로봇에게 이동 명령을 전송합니다.

## 📋 주요 기능 (Features)

* **실시간 손 인식:** MediaPipe Hands를 이용한 빠르고 정확한 손 랜드마크 추출
* **데이터 정규화:** 손의 거리나 위치에 상관없이 인식되도록 좌표 정규화 알고리즘(`func.py`) 적용
* **커스텀 데이터 학습:** 직접 데이터를 수집하고 SVM 모델을 학습시키는 파이프라인 제공
* **로봇 제어:** 인식 결과(가위/바위/보)에 따라 UR 로봇을 특정 조인트 각도로 이동
* **안전 장치:** 예측 정확도(Confidence)가 80% 이상일 때만 로봇 동작 명령 전송

## 🛠️ 기술 스택 (Tech Stack)

* **Language:** Python 3.x
* **Computer Vision:** OpenCV, MediaPipe
* **Machine Learning:** Scikit-learn (SVM), Joblib, Pandas, NumPy
* **Robot Communication:** Python Socket (TCP/IP for UR Script)

## 📂 파일 구조 (File Structure)

| 파일명 | 설명 |
| :--- | :--- |
| `point_to_csv.py` | 학습 데이터 수집용 스크립트. 웹캠을 켜고 키보드 입력(0, 1, 2)을 통해 랜드마크 데이터를 CSV로 저장합니다. |
| `model_train.py` | 수집된 `hand_data.csv`를 로드하여 SVM 모델을 학습시키고 `svm_hand_model.pkl`로 저장합니다. |
| `prediction_result.py` | **메인 실행 파일.** 실시간으로 제스처를 예측하고 실제 로봇(`no_wait.py`)을 제어합니다. |
| `prediction_result_real.py` | 테스트용 실행 파일. 로봇 연결 없이 예측 결과와 확률만 터미널에 출력합니다. |
| `no_wait.py` | 로봇과의 소켓 통신을 담당하는 모듈. 로봇 IP 설정 및 이동 명령(`movej`) 전송 기능을 포함합니다. |
| `func.py` | 좌표 정규화(`normalize_point`) 및 제스처 예측(`predict_gesture`)을 위한 유틸리티 함수 모음입니다. |
| `hand_data.csv` | `point_to_csv.py`를 통해 생성되는 학습 데이터 파일입니다. |

## 🚀 설치 및 실행 가이드 (Installation & Usage)

### 1. 라이브러리 설치
필요한 Python 라이브러리들을 설치합니다.

```bash
pip install opencv-python mediapipe scikit-learn pandas joblib numpy
```

### 2. 데이터 수집 (Data Collection)
`point_to_csv.py`를 실행하여 나만의 제스처 데이터를 수집합니다.
* 프로그램 실행 후 웹캠 창이 뜨면 손을 비춥니다.
* 원하는 손 모양을 만들고 **키보드 숫자 키**를 눌러 데이터를 저장합니다.
    * **0**: 가위 (Scissors)
    * **1**: 바위 (Rock)
    * **2**: 보 (Paper)
* 데이터는 `hand_data.csv` 파일에 누적되어 저장됩니다.

```bash
python point_to_csv.py
```

### 3. 모델 학습 (Model Training)
수집된 데이터를 바탕으로 SVM 모델을 학습합니다. 학습이 완료되면 `svm_hand_model.pkl` 파일이 생성됩니다.

```bash
python model_train.py
```

### 4. 로봇 연결 설정 (Robot Configuration)
`no_wait.py` 파일을 열어 로봇의 IP 주소를 환경에 맞게 수정합니다.

* **ROBOT_IP**: UR 로봇의 실제 IP 주소 (예: `192.168.0.31`)
* **PORT**: `30002` (UR 로봇 기본 포트)

```python
# no_wait.py
ROBOT_IP = "192.168.0.31"  # 실제 로봇 IP로 변경
PORT = 30002
```

### 5. 로봇 제어 실행 (Run Control)
`prediction_result.py`를 실행합니다.

* 프로그램이 시작되면 웹캠이 켜집니다.
* **키보드 '0' 키**를 누르면 현재 손 모양을 인식하고 예측을 수행합니다.
* 예측 확률(Confidence)이 **80% 이상**일 경우, 로봇이 해당 제스처에 매핑된 위치로 이동합니다.

```bash
python prediction_result.py
```

## 📊 로봇 동작 매핑 (Coordinates)

각 제스처에 대해 로봇은 미리 설정된 Joint 각도로 이동합니다. (`prediction_result.py` 내 설정)

* **가위 (0):** `[-46.20, -127.82, -22.93, -3.65, 85.72, -11.86]`
* **바위 (1):** `[-40.96, -86.23, -80.11, -91.88, 81.98, -7.28]`
* **보 (2):** `[-46.21, -87.65, -22.90, -76.80, 85.72, -11.86]`

## ⚠️ 안전 주의사항 (Safety Warning)

이 프로젝트는 실제 산업용 로봇을 제어합니다.

1.  **안전 거리 확보:** 로봇 주변에 충분한 안전 거리를 확보하세요.
2.  **속도 제한:** 테스트 시에는 로봇의 이동 속도(v)와 가속도(a)를 낮게 설정하는 것을 권장합니다.
3.  **비상 정지:** 비상 정지 버튼(E-Stop)을 항상 사용할 준비를 하십시오.
