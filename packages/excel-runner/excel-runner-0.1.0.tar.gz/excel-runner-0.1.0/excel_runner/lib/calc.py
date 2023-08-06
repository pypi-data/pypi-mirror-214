import os.path



def add(a, b):
    return a + b


def hello():
    file_path = os.path.join(os.path.dirname(__file__), 'a.txt')
    with open(file_path) as f:
        print(f.read())