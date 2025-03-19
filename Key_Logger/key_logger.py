from pynput import keyboard

def on_press(key):
    try:
        print(f'Alphanumeric key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')

def on_release(key):
    print(f'{key} released')
    if key == keyboard.Key.esc:
        return False  # Stop listener on ESC key

# Use the evdev backend for headless/non-GUI environments automatically
with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
    listener.join()
