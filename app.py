import os
import sys

from be import serve

file_dir = os.path.dirname(__file__)
print(file_dir)
sys.path.append(file_dir)

if __name__ == "__main__":
    serve.be_run()
