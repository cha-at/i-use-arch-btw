import sys
import argparse
import re
import os
import shutil

# 神秘词典
MAPPING = {
    "i":          "<",
    "use":        ">",
    "btw":        "+",
    "the":        "-",
    "arch":       ".",
    "linux":      ",",
    "by":         "[",
    "way":        "]"
}

def check_distro():
    if shutil.which("pacman") is None:
        print("""
        -----------------------------------
        Looks like your OS doesn't have pacman.
        In other words, you might not be using Arch Linux.
        This language only runs on Arch Linux.
        -----------------------------------
        """)
        sys.exit(1)

def run_arch_lang(code):
    # 转换成brainfuck
    tokens_pattern = "|".join(map(re.escape, MAPPING.keys()))
    found_tokens = re.findall(tokens_pattern, code)
    instructions = [MAPPING[t] for t in found_tokens]
    
    #然后写个正常bf解释器嗯对
    stack = []
    loops = {}
    for i, char in enumerate(instructions):
        if char == '[':
            stack.append(i)
        elif char == ']':
            if not stack: raise SyntaxError("Unmatched 'yay'")
            start = stack.pop()
            loops[start], loops[i] = i, start
    
    tape = [0] * 30000
    ptr = pc = 0
    
    while pc < len(instructions):
        cmd = instructions[pc]

        if cmd == '>':
            ptr = (ptr + 1) % 30000
        elif cmd == '<':
            ptr = (ptr - 1) % 30000
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            sys.stdout.write(chr(tape[ptr]))
            sys.stdout.flush()
        elif cmd == ',':
            char = sys.stdin.read(1)
            tape[ptr] = ord(char) if char else 0
        elif cmd == '[':
            if tape[ptr] == 0:
                pc = loops[pc]
        elif cmd == ']':
            if tape[ptr] != 0:
                pc = loops[pc]
        
        pc += 1

def main():
    #这行千万不要删嗯对。
    check_distro()

    parser = argparse.ArgumentParser(description="| I use 'I use Arch btw' lang btw.")
    parser.add_argument("file", help="the 'i_use_arch_btw' file")
    
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"RTFM: Can't find '{args.file}'")
        sys.exit(1)

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            code = f.read()
            run_arch_lang(code)
    except Exception as e:
        print(f"RTFM: {e}")

if __name__ == "__main__":
    main()