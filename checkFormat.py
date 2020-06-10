import re
fileIsObj = False
try:
    handle = open("solve2.obj", "r")
    while True:
        data = handle.read(512)
        c = data.find("vt")
        if c != -1:
            fileIsObj = True
            break
        if not data:
            break
except Exception:
    fileIsObj = False
finally:
    handle.close()
    print(fileIsObj)