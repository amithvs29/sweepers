import os


def safe_path(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
