import socket
import hashlib
import string
import itertools
import re
import sys

# 题目配置
HOST = "8.211.144.20"
PORT = 9999

def solve_pow(prefix, difficulty):
    """
    爆破计算满足条件的后缀
    """
    print(f"[-] 正在计算: sha256(\"{prefix}\" + ?) 前 {difficulty} 位为 0 ...")
    print("[-] 这可能需要几分钟，请耐心等待 (CPU 正在燃烧)...")
    
    # 字符集：字母+数字
    chars = string.ascii_letters + string.digits
    
    # 从长度 1 开始尝试，直到找到答案
    for length in range(1, 10):
        for s in itertools.product(chars, repeat=length):
            suffix = "".join(s)
            candidate = prefix + suffix
            # 计算 SHA256
            h = hashlib.sha256(candidate.encode()).hexdigest()
            # 转换为整数
            val = int(h, 16)
            # 检查前 N 位是否为 0
            # SHA256 是 256 位，要求前 difficulty 位为 0，即数值要小于 2^(256 - difficulty)
            if val < (1 << (256 - difficulty)):
                print(f"[+] 找到答案: {suffix}")
                return suffix

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print(f"[*] 已连接到 {HOST}:{PORT}")

        # 接收数据
        buffer = ""
        while "starts with" not in buffer:
            chunk = s.recv(4096).decode(errors='ignore')
            if not chunk:
                print("[!] 连接意外断开")
                return
            buffer += chunk
            
        print(f"[*] 收到题目:\n{buffer.strip()}")
        
        # 使用正则提取前缀和难度
        # 格式: sha256("GNJQEJ2PRz"+"?") starts with 26bits of zero:
        match = re.search(r'sha256\("(.+?)"\+"\?"\).*?(\d+)bits', buffer)
        
        if match:
            prefix = match.group(1)
            difficulty = int(match.group(2))
            
            # 开始计算
            ans = solve_pow(prefix, difficulty)
            
            # 发送答案
            print(f"[*] 发送答案: {ans}")
            s.sendall((ans + "\n").encode())
            
            # 读取服务器返回的 URL
            print("\n" + "="*30)
            print("服务器响应 (请复制下面的 URL):")
            print("="*30)
            
            while True:
                resp = s.recv(4096).decode(errors='ignore')
                if not resp:
                    break
                print(resp, end="")
        else:
            print("[!] 无法解析题目格式，请检查输出")

    except KeyboardInterrupt:
        print("\n[!] 用户停止")
    except Exception as e:
        print(f"\n[!] 发生错误: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    main()
