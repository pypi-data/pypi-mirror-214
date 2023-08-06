import os
import shutil

def array():
    return [1, 2, 3, 4, 5]

path = "./delete_me/"

if os.path.exists(path) and os.path.isdir(path):
    shutil.rmtree(path)
    print("Successfully deleted delete_me")
else:
    print("delete_me doesn't exist")
