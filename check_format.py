import traceback

import main
fileIsObj = False
try:
    file = main.solve
    handle = open(file, "r")
    while True:
        data = handle.read(512)
        c = data.find("vt")
        if c != -1:
            fileIsObj = True
            break
        if not data:
            break
    handle.close()
except Exception:
    print('File has to be obj format:\n', traceback.format_exc())
