import os

tests = {'semantictests.py', 'grammartests.py'}

code = 0
for test in tests:
    if os.system('python3 ' + test) == 1:
        code = 1
exit(code)
