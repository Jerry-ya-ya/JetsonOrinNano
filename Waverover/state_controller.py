from config import STATE_STOP, STATE_FORWARD, DANGER_FRAMES_REQUIRED, COOLDOWN_MS

class CarStateController:
    def __init__(self):
        self.current_state = STATE_STOP
        self.danger_frame_count = 0
        self.stop_triggered = False
        self.last_danger_ts = 0.0

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