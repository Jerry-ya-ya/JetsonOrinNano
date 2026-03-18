import cv2
import numpy as np
import time

CAM_INDEX = 0
WIDTH = 640
HEIGHT = 480

# 門檻可之後慢慢調
DANGER_THRESHOLD = 2.0
SAMPLE_STRIDE = 8
COOLDOWN_MS = 500

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

        mean_mag = float(np.mean(roi_sampled))
        max_mag = float(np.max(roi_sampled))

        now = time.time()
        is_danger = mean_mag >= DANGER_THRESHOLD

        if is_danger and (now - last_danger_ts) * 1000 >= COOLDOWN_MS:
            last_danger_ts = now
            print(f"[DANGER] mean={mean_mag:.3f}, max={max_mag:.3f}")

        status_text = "DANGER" if is_danger else "SAFE"
        color = (0, 0, 255) if is_danger else (0, 255, 0)

        # 畫出 ROI 區域
        x1, y1 = w // 4, h // 2
        x2, y2 = 3 * w // 4, h
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # 顯示數值
        cv2.putText(
            frame,
            f"{status_text} mean={mean_mag:.2f} max={max_mag:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        cv2.imshow("Optical Flow Collision Guard", frame)

        prev_gray = gray

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()