import time


def function_1():
    pass


def function_2():
    pass


def main():
    start_time = time.time()

    while time.time() < start_time + 0.25:
        function_1()
        function_2()


if __name__ == "__main__":
    main()
