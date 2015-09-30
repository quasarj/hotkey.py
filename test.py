import hotpy


def handle_f9():
    print("F9 Pressed")


def handle_f8():
    print("F8 Pressed, exiting now!")
    return False


def handle_c_f9():
    print("Control+F9 Pressed")


def test():
    print("Testing, press F9, Ctrl+F9, and F8 to exit")

    hotpy.register(handle_f9, 'F9')
    hotpy.register(handle_f8, 'F8')
    hotpy.register(handle_c_f9, 'F9', ['Ctrl'])
    hotpy.listen()


if __name__ == "__main__":
    test()
