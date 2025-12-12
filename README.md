import os

readme_content = """# 🖐️ Hand Gesture Controlled Dual Robot Arms (UR Robots)

이 프로젝트는 웹캠을 통해 손 제스처(가위, 바위, 보)를 인식하고, 인식된 결과에 따라 **두 대의 Universal Robot(UR)**을 동시에 제어하는 시스템입니다.

Google의 **MediaPipe**를 사용하여 손의 랜드마크를 추출하고, **SVM(Support Vector Machine)** 모델을 통해 제스처를 분류하며, **TCP/IP 소켓 통신**을 통해 각각의 로봇에게 지정된 좌표로 이동 명령을 전송합니다.

## 📋 주요 기능 (Features)

* **실시간 손 인식:** MediaPipe Hands를 이용한 빠르고 정확한 손 랜드마크 추출
* **듀얼 로봇 제어 (Multi-Robot Control):** 하나의 제스처 입력으로 두 대의 로봇(Robot 1, Robot 2)을 동시에 제어
* **데이터 정규화:** 손의 거리나 위치에 상관없이 인식되도록 좌표 정규화 알고리즘(`func.py`) 적용
* **커스텀 데이터 학습:** 직접 데이터를 수집하고 SVM 모델을 학습시키는 파이프라인 제공
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
| `prediction_result.py` | **메인 실행 파일.** 두 대의 로봇 IP(`ip_1`, `ip_2`)를 설정하고, 제스처에 따라 각각의 로봇을 제어합니다. |
| `prediction_result_real.py` | 테스트용 실행 파일. 로봇 연결 없이 예측 결과와 확률만 터미널에 출력합니다. |
| `no_wait.py` | 로봇과의 소켓 통신 모듈. IP를 인자로 받아 `movej` 명령을 전송하도록 개선되었습니다. |
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
* 웹캠이 켜지면 원하는 손 모양을 만들고 **키보드 숫자 키**를 누릅니다.
    * **0**: 가위 (Scissors)
    * **1**: 바위 (Rock)
    * **2**: 보 (Paper)
* 데이터는 `hand_data.csv`에 저장됩니다.

```bash
python point_to_csv.py
```

### 3. 모델 학습 (Model Training)
수집된 데이터를 바탕으로 SVM 모델을 학습합니다.

```bash
python model_train.py
```

### 4. 로봇 IP 설정 (Configuration)
**변경된 점:** 이제 `no_wait.py`가 아닌 `prediction_result.py`에서 두 로봇의 IP를 직접 설정합니다.

`prediction_result.py` 파일을 열어 아래 변수를 수정하세요.

```python
# prediction_result.py 내부
ip_1 = "192.168.0.31"  # 첫 번째 로봇 IP
ip_2 = "192.168.0.40"  # 두 번째 로봇 IP
```

### 5. 듀얼 로봇 제어 실행 (Run Control)
`prediction_result.py`를 실행합니다.

* **키보드 '0' 키**를 누르면 현재 손 모양을 인식합니다.
* 예측 확률이 **80% 이상**일 경우, 두 로봇이 각각 설정된 위치로 동시에 이동합니다.

```bash
python prediction_result.py
```

## 📊 로봇 동작 매핑 (Dual Coordinates)

각 제스처 인식 시 두 로봇은 서로 다른 Joint 각도로 이동하여 협동 동작을 수행합니다.

| 제스처 | Robot 1 (ip_1) 동작 | Robot 2 (ip_2) 동작 |
| :--- | :--- | :--- |
| **가위 (0)** | `[-40.96, -86.11, -6.61, -91.87, 81.98, -7.28]` | `[50.78, -97.04, 20.88, -106.91, -95.23, -184.14]` |
| **바위 (1)** | `[-43.20, -66.50, -86.76, -171.44, 96.23, 1.42]` | `[40.75, -136.46, 89.05, -14.58, -99.71, -177.51]` |
| **보 (2)** | `[-136.76, -62.32, -86.71, ...]` | `...` (설정된 좌표로 이동) |

> *좌표 수정은 `prediction_result.py` 파일 내 `deg_values_1`, `deg_values_2` 리스트를 변경하세요.*

## ⚠️ 안전 주의사항 (Safety Warning)

**두 대의 로봇이 동시에 움직입니다.**
1.  **충돌 방지:** 두 로봇 간의 작업 반경이 겹치지 않는지, 혹은 협업 시 충돌 가능성이 없는지 반드시 확인하세요.
2.  **비상 정지:** 두 로봇의 비상 정지(E-Stop) 버튼 위치를 모두 파악하고 있어야 합니다.
3.  **속도 제한:** 초기 테스트 시에는 가속도와 속도를 낮춰서 실행하세요.
"""

file_path = "README.md"

try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✅ '{file_path}' 파일이 업데이트된 내용(듀얼 로봇)으로 생성되었습니다!")
except Exception as e:
    print(f"❌ 파일 생성 중 오류가 발생했습니다: {e}")