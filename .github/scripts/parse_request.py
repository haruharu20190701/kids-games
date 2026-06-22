#!/usr/bin/env python3
# 依頼ファイル（imagegen-requests/request.txt）を読み、
#   ヘッダ（kind/dest/size/transparent）を GITHUB_ENV 形式で標準出力へ、
#   プロンプト本文を 第2引数のファイルへ書き出す。
# 使い方: python3 parse_request.py <request.txt> <out_prompts.txt>
#
# 依頼ファイルの形式（'---' の前がヘッダ、後ろがプロンプト。--- が無ければ全部プロンプト）:
#   kind: custom
#   dest: games/mole/assets
#   size: 512
#   transparent: true
#   ---
#   slug | プロンプト
#   slug2 | プロンプト
import sys

req, out = sys.argv[1], sys.argv[2]
kind, dest, size, transparent = "icon", "", "512", "false"

with open(req, encoding="utf-8") as f:
    lines = f.read().splitlines()

if "---" in lines:
    sep = lines.index("---")
    header, body = lines[:sep], lines[sep + 1:]
else:
    header, body = [], lines

for ln in header:
    s = ln.strip()
    if not s or s.startswith("#") or ":" not in s:
        continue
    k, v = s.split(":", 1)
    k, v = k.strip().lower(), v.strip()
    if k == "kind":
        kind = v
    elif k == "dest":
        dest = v
    elif k == "size":
        size = v
    elif k == "transparent":
        transparent = "true" if v.lower() in ("true", "1", "yes", "on") else "false"

prompts = [ln for ln in body if ln.strip() and not ln.strip().startswith("#")]
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(prompts) + "\n")

print(f"KIND={kind}")
print(f"DEST_IN={dest}")
print(f"SIZE_IN={size}")
print(f"TRANSPARENT={transparent}")
