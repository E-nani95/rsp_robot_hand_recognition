import math
import numpy as np




def target_distance(wrist_point, MCL_point):
    base_distance = math.dist([wrist_point.x,wrist_point.y],[MCL_point.x,MCL_point.y])
    return base_distance

def normalize_point(landmark):
    wrist_point = landmark.landmark[0]
    mcp_point = landmark.landmark[9]
    base_distance = target_distance(wrist_point,mcp_point)

    n_data=[]

    for target_point in  landmark.landmark:
        x_point=target_point.x-wrist_point.x
        y_point=target_point.y-wrist_point.y
        x_point=x_point/base_distance
        y_point=y_point/base_distance

        n_data.append(x_point)
        n_data.append(y_point)
    return n_data


def predict_gesture(normalized_list,loaded_model):
    # 2. 모델에 넣기 위해 형태 변환 (1줄짜리 2차원 배열로)
    # Scikit-Learn은 입력으로 [[데이터]] 형태를 원합니다.
    input_data = np.array([normalized_list])

    # 3. 예측 (0:가위, 1:바위, 2:보)
    prediction = loaded_model.predict(input_data)

    # 4. 확률도 확인 가능 (예: 가위일 확률 98%)
    proba = loaded_model.predict_proba(input_data)
    confidence = np.max(proba)  # 가장 높은 확률값

    return prediction[0], confidence ,proba