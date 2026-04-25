from pynput import keyboard
from config import KEYBOARD_SPEED_STEP, KEYBOARD_TURN_STEP

def create_keyboard_listener(controller):
    def on_press(key):
        try:
            if key.char == "m":
                controller.enter_keyboard_manual()

            elif key.char == "s":
                controller.stop_manual()

        except AttributeError:
            if key == keyboard.Key.up:
                controller.adjust_manual_drive(
                    KEYBOARD_SPEED_STEP,
                    KEYBOARD_SPEED_STEP
                )

            elif key == keyboard.Key.down:
                controller.adjust_manual_drive(
                    -KEYBOARD_SPEED_STEP,
                    -KEYBOARD_SPEED_STEP
                )

            elif key == keyboard.Key.left:
                controller.adjust_manual_drive(
                    -KEYBOARD_TURN_STEP,
                    KEYBOARD_TURN_STEP
                )

            elif key == keyboard.Key.right:
                controller.adjust_manual_drive(
                    KEYBOARD_TURN_STEP,
                    -KEYBOARD_TURN_STEP
                )

            elif key == keyboard.Key.space:
                controller.stop_manual()

    return keyboard.Listener(on_press=on_press)