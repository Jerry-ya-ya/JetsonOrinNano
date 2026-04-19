import cv2
import numpy as np
import time
from pynput import mouse

from config import CAM_INDEX, WIDTH, HEIGHT, DANGER_THRESHOLD, SAMPLE_STRIDE, COOLDOWN_MS, DANGER_FRAMES_REQUIRED, SERIAL_PORT, BAUDRATE, STATE_STOP, STATE_FORWARD
from motor_serial import init_serial, send_forward, send_stop

def trigger_stop(ser):
    if ser is None:
        print(">>> STOP COMMAND TRIGGERED <<< but serial is not available")
        return
    send_stop(ser)
    print(">>> STOP COMMAND TRIGGERED <<<")
    
def main():
    ser = init_serial()
    if ser is None:
        raise RuntimeError("Failed to initialize serial")

    current_state = STATE_STOP
    danger_frame_count = 0
    stop_triggered = False
    last_danger_ts = 0.0

    def toggle_state():
        nonlocal current_state, stop_triggered

        # 如果目前在危險停止狀態，就先不允許前進
        if stop_triggered:
            print("Blocked: danger stop is active")
            return

        if current_state == STATE_STOP:
            current_state = STATE_FORWARD
            send_forward(ser)
            print("STATE -> FORWARD")
        else:
            current_state = STATE_STOP
            send_stop(ser)
            print("STATE -> STOP")

    def on_click(x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            toggle_state()

    listener = mouse.Listener(on_click=on_click)
    listener.start()

    send_stop(ser)
    print("Initial state: STOP")

    cap = cv2.VideoCapture(CAM_INDEX)

    if not cap.isOpened():
        listener.stop()
        ser.close()
        raise RuntimeError("Cannot open camera")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    ret, frame = cap.read()
    if not ret:
        listener.stop()
        cap.release()
        ser.close()
        raise RuntimeError("Failed to read first frame")

    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Failed to read frame")
            time.sleep(0.1)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, gray, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )

        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        h, w = mag.shape
        roi = mag[h // 2:h, w // 4: 3 * w // 4]
        roi_sampled = roi[::SAMPLE_STRIDE, ::SAMPLE_STRIDE]

        mean_mag = float(np.mean(roi_sampled))
        max_mag = float(np.max(roi_sampled))
        now = time.time()

        is_danger = mean_mag >= DANGER_THRESHOLD

        if is_danger:
            danger_frame_count += 1
        else:
            danger_frame_count = 0

        confirmed_danger = danger_frame_count >= DANGER_FRAMES_REQUIRED

        if confirmed_danger and not stop_triggered and (now - last_danger_ts) * 1000 >= COOLDOWN_MS:
            stop_triggered = True
            last_danger_ts = now

            # 危險停車時，狀態機也要同步回 STOP
            current_state = STATE_STOP

            print(f"[DANGER] mean={mean_mag:.3f}, max={max_mag:.3f}, count={danger_frame_count}")
            trigger_stop(ser)

        if not confirmed_danger:
            stop_triggered = False

        status_text = "DANGER" if confirmed_danger else "SAFE"
        color = (0, 0, 255) if confirmed_danger else (0, 255, 0)

        x1, y1 = w // 4, h // 2
        x2, y2 = 3 * w // 4, h
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        cv2.putText(
            frame,
            f"{status_text} mean={mean_mag:.2f} max={max_mag:.2f} count={danger_frame_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        state_name = "FORWARD" if current_state == STATE_FORWARD else "STOP"
        cv2.putText(
            frame,
            f"STATE: {state_name}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        if stop_triggered:
            cv2.putText(
                frame,
                "STOPPED BY DANGER",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        cv2.imshow("Optical Flow Collision Guard", frame)

        prev_gray = gray

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    listener.stop()
    cap.release()
    cv2.destroyAllWindows()
    ser.close()

if __name__ == "__main__":
    main()