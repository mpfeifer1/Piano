import os
tests = {'semantictests.py', 'grammartests.py'}
for test in tests:
    os.system('python3 ' + test)
