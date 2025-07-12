import sys

if len(sys.argv) == 2:
    name = sys.argv[1]
    print(f"hello, {name}")
else:
    print("hello, world")