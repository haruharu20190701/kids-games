#!/usr/bin/env python3
# 白背景を透明に抜く（外周の白だけ＝黒い輪郭線で囲まれた素材向け）。
# 四隅からフラッドフィルして「外側につながった白」だけα=0にするので、
# 主題の中の白（目・ハイライト等）は黒線に守られて残る。
# 使い方: python3 transify.py <in.png> <out.png> [thresh=60]
import sys
from PIL import Image, ImageDraw

def main():
    if len(sys.argv) < 3:
        print("usage: transify.py <in.png> <out.png> [thresh]", file=sys.stderr)
        sys.exit(2)
    src, out = sys.argv[1], sys.argv[2]
    thresh = int(sys.argv[3]) if len(sys.argv) > 3 else 60

    im = Image.open(src).convert("RGBA")
    w, h = im.size
    rgb = im.convert("RGB")
    SENT = (255, 0, 255)  # 一時マーカー色（出力には残さない）
    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        ImageDraw.floodfill(rgb, seed, SENT, thresh=thresh)
    src_px, dst_px = rgb.load(), im.load()
    cnt = 0
    for y in range(h):
        for x in range(w):
            if src_px[x, y] == SENT:
                r, g, b, _ = dst_px[x, y]
                dst_px[x, y] = (r, g, b, 0)
                cnt += 1
    im.save(out)
    print(f"透明化: {cnt}/{w*h} px をα=0に → {out}")

if __name__ == "__main__":
    main()
