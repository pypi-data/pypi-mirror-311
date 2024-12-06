import os
import shutil

def deleteAllCache(directory: str) -> None: # by ChatGPT :)
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            if name.endswith(('.pyc', '.cashe', '.pyo')):
                file_path = os.path.join(root, name)
                try:
                    os.remove(file_path)
                except Exception as e: ...
        
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                if name == "__pycache__":
                    shutil.rmtree(dir_path)
            except Exception as e: ...

if __name__ == '__main__':
    deleteAllCache(os.path.dirname(__file__))