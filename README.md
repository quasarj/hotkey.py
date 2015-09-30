# hotpy
Python module for easily binding hotkeys in Windows.

There are a few other libraries out there that do this, but none of them seem to work with Python 3.4+, so hotpy was born.

```python
import hotpy


def handle_f9():
    print("F9 Pressed")


def exit():
    return False  # if a callback returns false, hotpy.listen() exits


hotpy.register(handle_f9, 'F9')
hotpy.register(exit, 'F9', ['Ctrl', 'Shift'])
hotpy.listen()
```

See the source for a list of valid key and modifier names.

The idea and a portion of the code came from: https://github.com/schurpf/pyhk

## Requirements
* Python 3.x (only tested on 3.4+)
* py32win

## License
GPLv2
