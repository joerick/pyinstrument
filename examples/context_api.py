import os
import pprint
import sys
import time

pprint.pprint(sys.path)
import pyinstrument


@pyinstrument.profile()
def main():
    py_file_count = 0
    py_file_size = 0

    print("Start.")
    print("scanning home dir...")

    with pyinstrument.profile():
        for dir_path, dirnames, filenames in os.walk(os.path.expanduser("~/Music")):
            for filename in filenames:
                file_path = os.path.join(dir_path, filename)
                _, ext = os.path.splitext(file_path)
                if ext == ".py":
                    py_file_count += 1
                    try:
                        py_file_size += os.stat(file_path).st_size
                    except:
                        pass

    print("There are {} python files on your system.".format(py_file_count))
    print("Total size: {} kB".format(py_file_size / 1024))


class A:
    @pyinstrument.profile()
    def foo(self):
        time.sleep(0.1)


if __name__ == "__main__":
    a = A()
    a.foo()
    main()
