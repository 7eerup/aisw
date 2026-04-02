import os

path = "/home/claude/aisw/python/data/hello.txt"

with open(path, "r", encoding="utf-8") as f:
    print("파일 내용:", f.read())

print("\n전체 경로  :", os.path.abspath(path))
print("폴더 경로  :", os.path.dirname(path))
print("파일 이름  :", os.path.basename(path))
print("현재 위치  :", os.getcwd())



# import os

# with open("./data/hello.txt", "r", encoding="utf-8") as f:
#     print("파일 내용:", f.read())

# print("현재 위치 :", os.getcwd())