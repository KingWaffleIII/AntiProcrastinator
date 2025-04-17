import json
import os

with open("assets.json") as json_file:
    json_data = json_file.read()
    assets = json.loads(json_data)

# copy assets into dist/AntiProcrastinator/data
for asset in assets:
    src = os.path.join(os.getcwd(), asset)
    dst = os.path.join("dist", "AntiProcrastinator", "data", asset)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
        fdst.write(fsrc.read())
