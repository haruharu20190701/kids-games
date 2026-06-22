# imagegen-requests — リモートから画像生成を起動する「依頼ファイル」

リモートのClaude（や誰でも書き込み権限のある人）が、**`request.txt` を書いて push する**と
`.github/workflows/generate-images.yml` が自動起動し、PCのセルフホストランナーで画像を生成→
縮小→（任意で透明化）→ `icons/` や指定フォルダへ自動コミットする。

`gh workflow run`（workflow_dispatch）の権限が無いリモート環境でも、**コミット権限さえあれば起動できる**のが狙い。

## request.txt の形式
`---` の前がヘッダ、後ろがプロンプト（`slug | プロンプト` を1行ずつ）。

```
kind: custom            # icon / coloring / custom
dest: games/mole/assets # kind=custom のときの保存先（リポジトリ相対・.. 不可）
size: 512               # kind=custom のときの長辺px
transparent: true       # 白背景を透明化するなら true（黒枠で囲まれた素材向け）
---
mole | cute kawaii flat vector of a happy mole, ... plain pure white background, no text
rabbit | cute kawaii flat vector of a happy rabbit, ... plain pure white background, no text
```

- `kind=icon` は `icons/<slug>.png`（256px）、`kind=coloring` は `games/coloring/lines/<slug>.png`（900px）に保存（その場合 dest/size は無視）。
- 生成後の**ゲームへの登録**（`PICS`/`GAMES`/各ゲームHTMLへの組み込み）はワークフローはやらない。Claudeが別途コードを編集する。

## 注意
- トリガーは **main の `imagegen-requests/request.txt` への push のみ**。fork からは main に push できないので安全。
- ランナーが起動している必要あり（`~/kids-runner` の launchd 常駐）。停止中は run が queued のまま。
- 同じ依頼を再実行したい（作り直したい）ときは、プロンプトを少し変える（同一行は生成済みスキップ）。
