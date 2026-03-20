import cv2
import numpy as np
import time

# 攝影機參數設定
CAM_INDEX = 0
WIDTH = 640
HEIGHT = 480

# 危險門檻設定
DANGER_THRESHOLD = 2.0
SAMPLE_STRIDE = 8
COOLDOWN_MS = 500

# 最大危險幀與危險幀連續數量的設定，避免誤判
DANGER_FRAMES_REQUIRED = 3
danger_frame_count = 0

# 狀態鎖避免每一幀都觸發 stop指令
stop_triggered = False

# 危險停車函數
def trigger_stop():
    print(">>> STOP COMMAND TRIGGERED <<<")

# 主要判斷與攝影機開啟函數
def main():
    cap = cv2.VideoCapture(CAM_INDEX)

    if not cap.isOpened():
        raise RuntimeError("Cannot open camera")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to read first frame")

    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    last_danger_ts = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Failed to read frame")
            time.sleep(0.1)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 計算 dense optical flow
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, gray, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )

        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        h, w = mag.shape

        # 只看下半部 + 中間區域，較像前方碰撞區
        roi = mag[h // 2:h, w // 4: 3 * w // 4]
        roi_sampled = roi[::SAMPLE_STRIDE, ::SAMPLE_STRIDE]

        # 計算平均與最大光流 magnitude
        mean_mag = float(np.mean(roi_sampled))
        max_mag = float(np.max(roi_sampled))

        now = time.time()

        # 單幀判斷是否危險
        is_danger = mean_mag >= DANGER_THRESHOLD

        # 更新連續危險幀計數
        if is_danger:
            danger_frame_count += 1
        else:
            danger_frame_count = 0
        
        # 連續 3 幀危險，才真的算危險
        confirmed_danger = danger_frame_count >= DANGER_FRAMES_REQUIRED

        # 每次確認危險且冷卻時間過後，觸發停車指令
        if confirmed_danger and not stop_triggered:
            stop_triggered = True
            last_danger_ts = now

            print(f"[DANGER] mean={mean_mag:.3f}, max={max_mag:.3f}, count={danger_frame_count}")
            trigger_stop()
        
        # 如果不再危險，重置狀態
        if not confirmed_danger:
            stop_triggered = False
        
        # 狀態文字與顏色設定
        status_text = "DANGER" if confirmed_danger else "SAFE"
        color = (0, 0, 255) if confirmed_danger else (0, 255, 0)

        # 畫出 ROI 區域
        x1, y1 = w // 4, h // 2
        x2, y2 = 3 * w // 4, h
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # 顯示數值
        cv2.putText(
            frame,
            f"{status_text} mean={mean_mag:.2f} max={max_mag:.2f} count={danger_frame_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )
        
        if stop_triggered:
            cv2.putText(
                frame,
                "STOPPED",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # 顯示結果
        cv2.imshow("Optical Flow Collision Guard", frame)
        
        # 更新前一幀灰階圖
        prev_gray = gray

        # 檢查退出條件
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break
    # 釋放資源
    cap.release()
    cv2.destroyAllWindows()
# 程式入口
if __name__ == "__main__":
    main()