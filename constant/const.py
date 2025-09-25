import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MISC_PATH = os.path.join(BASE_PATH, 'misc')

if __name__ == '__main__':
    print(BASE_PATH)
