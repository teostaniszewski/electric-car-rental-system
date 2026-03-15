import os

def what(file, h=None):
    ext = os.path.splitext(file)[1].lower()

    if ext == ".gif":
        return "gif"
    elif ext == ".png":
        return "png"
    elif ext == ".jpg" or ext == ".jpeg":
        return "jpeg"
    elif ext == ".bmp":
        return "bmp"
    elif ext == ".ico":
        return "ico"

    return None