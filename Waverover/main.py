import cv2
import numpy as np
import time
import pynput.keyboard as keyboard
import config

from motor_serial import init_serial, send_stop, send_forward, send_drive
from state_controller import CarStateController
from mouse_listener import create_mouse_listener
from keyboard_listener import create_keyboard_listener

def main():
    ser = init_serial()
    if ser is None:
        raise RuntimeError("Failed to initialize serial")
    
    controller = CarStateController()

    mouse_listener = create_mouse_listener(controller, send_forward, send_stop, ser)
    mouse_listener.start()

    keyboard_listener = create_keyboard_listener(controller)
    keyboard_listener.start()

    send_stop(ser)
    print("Initial state: STOP")

    cap = cv2.VideoCapture(config.CAM_INDEX)

    if not cap.isOpened():
        mouse_listener.stop()
        keyboard_listener.stop()
        ser.close()
        raise RuntimeError("Cannot open camera")
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.HEIGHT)

    ret, frame = cap.read()
    if not ret:
        mouse_listener.stop()
        keyboard_listener.stop()
        cap.release()
        ser.close()
        raise RuntimeError("Failed to read first frame")
    
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    last_manual_send_time = 0.0

    last_left = None
    last_right = None

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
        roi_sampled = roi[::config.SAMPLE_STRIDE, ::config.SAMPLE_STRIDE]

        mean_mag = float(np.mean(roi_sampled))
        max_mag = float(np.max(roi_sampled))
        now = time.time()

        is_danger = mean_mag >= config.DANGER_THRESHOLD

        confirmed_danger = controller.update_danger(is_danger, now, mean_mag, max_mag, send_stop, ser)

        status_text = "SAFE"

        now = time.time()

        if controller.current_state == config.STATE_KEYBOARD_MANUAL and not controller.stop_triggered:
            left = controller.manual_left
            right = controller.manual_right

            changed = (left != last_left) or (right != last_right)
            timeout = (now - last_manual_send_time >= config.MANUAL_SEND_INTERVAL)

            if changed or timeout:
                send_drive(ser, left, right)
                last_manual_send_time = now
                last_left = left
                last_right = right
        
        color = (0, 0, 255) if confirmed_danger else (0, 255, 0)

        x1, y1 = w // 4, h // 2
        x2, y2 = 3 * w // 4, h
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        cv2.putText(
            frame,
            f"{status_text} mean={mean_mag:.2f} max={max_mag:.2f} count={controller.danger_frame_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        state_name = "FORWARD" if controller.current_state == config.STATE_FORWARD else "STOP"
        cv2.putText(
            frame,
            f"STATE: {state_name}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        if controller.stop_triggered:
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
        if key == ord('t'):
            print("Key 't' pressed, attempting to toggle state")
            controller.toggle_state(send_forward, send_stop, ser)
        elif key == 27 or key == ord('q'):
            break

    mouse_listener.stop()
    keyboard_listener.stop()

    cap.release()
    cv2.destroyAllWindows()
    ser.close()

if __name__ == "__main__":
    main()