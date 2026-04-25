from config import (
    STATE_STOP,
    STATE_FORWARD,
    DANGER_FRAMES_REQUIRED,
    STATE_KEYBOARD_MANUAL,
    COOLDOWN_MS,
    MAX_SPEED,
    MIN_SPEED)

class CarStateController:
    def __init__(self):
        self.current_state = STATE_STOP
        self.danger_frame_count = 0
        self.stop_triggered = False
        self.last_danger_ts = 0.0
        self.manual_left = 0.0
        self.manual_right = 0.0

    def toggle_state(self, send_forward, send_stop, ser):
        # 如果目前在危險停止狀態，就先不允許前進
        if self.stop_triggered:
            print("Blocked: danger stop is active")
            return

        if self.current_state == STATE_STOP:
            self.current_state = STATE_FORWARD
            send_forward(ser)
            print("STATE -> FORWARD")
        else:
            self.current_state = STATE_STOP
            send_stop(ser)
            print("STATE -> STOP")
    
    def update_danger(self, is_danger, now, mean_mag, max_mag, trigger_stop, ser):
        if is_danger:
            self.danger_frame_count += 1
        else:
            self.danger_frame_count = 0

        confirmed_danger = self.danger_frame_count >= DANGER_FRAMES_REQUIRED
        
        if confirmed_danger and not self.stop_triggered and (now - self.last_danger_ts) * 1000 >= COOLDOWN_MS:
            self.stop_triggered = True
            self.last_danger_ts = now
            # 危險停車時，狀態機也要同步回 STOP
            self.current_state = STATE_STOP

            print(f"[DANGER] mean={mean_mag:.3f}, max={max_mag:.3f}, count={self.danger_frame_count}")
            
            trigger_stop(ser)

        if not confirmed_danger:
            self.stop_triggered = False
        return confirmed_danger
    def enter_keyboard_manual(self):
        if self.stop_triggered:
            print("Blocked: danger stop is active")
            return

        self.current_state = STATE_KEYBOARD_MANUAL
        self.manual_left = 0.0
        self.manual_right = 0.0
        print("STATE -> KEYBOARD_MANUAL")

    def stop_manual(self):
        self.current_state = STATE_STOP
        self.manual_left = 0.0
        self.manual_right = 0.0
        print("STATE -> STOP")
        
    def adjust_manual_drive(self, delta_left, delta_right):
        if self.current_state != STATE_KEYBOARD_MANUAL:
            return

        self.manual_left += delta_left
        self.manual_right += delta_right

        self.manual_left = max(MIN_SPEED, min(MAX_SPEED, self.manual_left))
        self.manual_right = max(MIN_SPEED, min(MAX_SPEED, self.manual_right))

        print(f"MANUAL L={self.manual_left:.2f}, R={self.manual_right:.2f}")