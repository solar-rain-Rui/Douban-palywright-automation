import sys
import os

print("当前工作目录:", os.getcwd())
print("\nsys.path:")
for p in sys.path:
    print(p)

# 测试能否 import pages
print("\n尝试 import pages:")
try:
    import pages
    print("成功：可以 import pages")
except Exception as e:
    print("失败：", e)
