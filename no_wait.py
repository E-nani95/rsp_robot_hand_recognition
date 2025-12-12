import socket
import time
import math
# -----------------------------------------------------------
# [설정] 로봇 IP와 포트
# -----------------------------------------------------------
#ROBOT_IP = "192.168.0.31"
PORT = 30002

# -----------------------------------------------------------
# [중요] Waypoint S의 좌표 설정
# 로봇 티칭 팬던트의 [Move] 탭에서 현재 관절 각도를 확인 후 입력하세요.
# 형식: [Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3] (단위: 라디안)
# 예시: 모든 관절이 0이거나 90도(-1.57)인 상태
# -----------------------------------------------------------
# deg_values = [-40.96, -86.23, -80.11, -91.88, 81.98, -7.28]
# waypoint_s = [math.radians(d) for d in deg_values]

def move_robot(deg_values, ROBOT_IP):
    print(f"[{ROBOT_IP}:{PORT}] 로봇 이동 명령 연결 시도...")
    waypoint_s = [math.radians(d) for d in deg_values]
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)
        sock.connect((ROBOT_IP, PORT))
        print(">> 소켓 연결 성공 (TCP Connected)")

        # 1. 초기 데이터 수신 (버퍼 비우기)
        try:
            sock.recv(1024)
        except:
            pass

        # 2. 이동 명령 스크립트 작성 (URScript)
        # movej(q, a=가속도, v=속도, t=시간, r=블렌드반경)
        # a=1.0 rad/s^2, v=0.5 rad/s (테스트를 위해 천천히 설정함)

        # 파이썬 리스트를 URScript 배열 문자열로 변환
        target_q = str(waypoint_s)

        script = f"movej({target_q}, a=1.0, v=0.5)\n"

        print(f">> 명령 전송: {script.strip()}")
        sock.send(script.encode())

        # 명령이 로봇에 도달할 시간을 잠깐 줍니다
        time.sleep(1)
        print(">> 전송 완료. 로봇이 움직이는지 확인하세요.")

    except Exception as e:
        print(f"!! 연결 또는 전송 에러: {e}")

    finally:
        if sock:
            sock.close()


if __name__ == "__main__":
    move_robot()