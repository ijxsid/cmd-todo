import sys
import os.path
import time
# HACK: To make lib accesible here.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from lib.utils import MOVE_CURSOR_UP

def main():
    print("start")
    for i in range(100):

        print('{}'.format('goto ' + str(i)))
        sys.stdout.write(MOVE_CURSOR_UP)
        time.sleep(1)
    print

if __name__ == '__main__':
    main()
