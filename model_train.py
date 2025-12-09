import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib

file_name = 'hand_data.csv'

data=pd.read_csv(file_name)
print("Load Success")

# 전처리

x = data.drop('label',axis=1)
y = data['label']

x_train,x_test,y_train,y_test=train_test_split(x,y, test_size=0.2, stratify=y)

#학습
# 정규화 잘되면 Linear 쓰면 잘안됨
# Linear 안되면 rbf <- 이게 default 값
model = SVC(kernel='linear', probability=True)
model.fit(x_train, y_train)

#평가
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test,y_pred)

print("-" * 30)
print(f"모델 정확도: {accuracy * 100:.2f}%")
print("-" * 30)
print("분류 보고서:")
print(classification_report(y_test, y_pred))

#저장
model_filename = 'svm_hand_model.pkl'
joblib.dump(model, model_filename)

print(f"모델이 '{model_filename}' 파일로 저장되었습니다.")