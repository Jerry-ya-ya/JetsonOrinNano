from pynput import mouse

def create_mouse_listener(controller, send_forward, send_stop, ser):
    def on_click(x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            print("Mouse clicked, attempting to toggle state")
            controller.toggle_state(send_forward, send_stop, ser)

    return mouse.Listener(on_click=on_click)