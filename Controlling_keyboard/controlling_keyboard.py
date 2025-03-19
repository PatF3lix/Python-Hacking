from pynput.keyboard import Key, Controller

keyboard = Controller()

# Presss and release space
keyboard.press(Key.space)
keyboard.release(Key.space)

# Type a lower case A; this will work even if no key on the
#  physical keyboard is llabelled 'A'
keyboard.press('a')
keyboard.release('a')

# type two upper case As
keyboard.press('A')
keyboard.release('A')
with keyboard.pressed(Key.shift):
    keyboard.press('a')
    keyboard.release('a')

# Type 'Hello World using the shortcut type method
keyboard.type('Hello World')