# CLAUDE.md

このリポジトリで Claude Code が作業するためのガイド。

## これは何か
**こどもあそびば** — 5歳前後の子供向けのブラウザゲーム集。
**外部ライブラリ・ビルド不要のピュアな静的HTML/CSS/JS**。GitHub Pages で無料公開。

- 公開サイト: https://haruharu20190701.github.io/kids-games/
- リポジトリ: https://github.com/haruharu20190701/kids-games （アカウント: **haruharu20190701**）

## 構成
```
kids/
├── index.html              ゲーム選択メニュー（ランチャー・データ駆動）
├── games/<slug>/index.html 1ゲーム＝1フォルダ＝1ファイル完結
│   ├── puzzle-block/        ぱずるぶろっく（ステージ制パズル）
│   ├── piano/              ぴあの（自由演奏＋おてほん曲）
│   ├── draw/               おえかき（自由描画・スタンプ）
│   ├── memory/             しんけいすいじゃく（神経衰弱）
│   ├── numbers/            かずあそび（数を数える）
│   ├── airhockey/          エアホッケー（CPU/2人・物理）
│   └── coloring/           ぬりえ（バケツ塗り・選択→ぬる画面）
│       └── lines/          ぬりえの線画（画像）。例 dino.png
├── shared/                 （将来）共通CSS/JS
├── robots.txt              全クロール許可＋sitemap の場所を明示
├── sitemap.xml             公開ページ一覧（ゲーム追加時に1 URL追記）
├── icon-1024.png / icon-180.png  ホーム画面・OGP用アイコン
├── README.md               利用者向けの概要・追加手順
├── PROJECT.md              プロジェクトの目的・学び・ロードマップ
└── .gitignore              .claude/ など非公開物を除外
```

## 基本ルール（ゲームの追加・編集はこれに従う）
- **1ゲーム = 1ファイル**: `games/<slug>/index.html` にHTML/CSS/JSを全部入れる。バンドラ・npm・CDNライブラリは使わない（軽量・オフライン可）。
- **対象は約5歳**: ひらがな表記、大きなタップ領域、時間制限なし、失敗にやさしい、「できた！」の演出を厚く。
- **音は Web Audio API**（オシレータのbeep）。音声ファイルは使わない（アセットゼロ）。
- **入力はタッチ＆マウス両対応**（touchstart/mousedown 等の両方を張る）。
- **モバイル前提**: `viewport`(user-scalable=no)、`touch-action:none`、`100dvh`、`box-sizing:border-box`。
- コード内コメントは既存に合わせて**ひらがな日本語**。

## 新しいゲームの追加
1. `games/<slug>/index.html` を作る（slug = 半角小文字。例 `numbers`, `memory-card`）。
2. 🏠ホームボタン（`../../index.html`）と、結果画面に「メニューへ」リンクを置く。
3. **`<head>` に最小SEOタグを入れる**（下の「最小SEO」テンプレ参照。`<title>` / `description` / `canonical` / OGP）。
4. ルート `index.html` の `GAMES` 配列に登録: `{ name, emoji, path }`。
5. **`sitemap.xml` に新ページの `<url>` を1ブロック追記**（メニュー登録と sitemap は必ず一致させる）。
6. テスト → コミット → プッシュ。
- スキル `/new-kids-game` で手順を呼び出せる。
- ⚠️ メニュー登録・sitemap・head の SEO は3点セット。どれか1つだけ漏れがちなので追加時に必ず揃える。

## ローカル開発・テスト
- **`file://` はテスト用ブラウザでブロックされる**。必ずHTTPで配信:
  `python3 -m http.server 8000` → `http://localhost:8000/...`
- 実機サイズで確認: スマホ縦 390×844 / スマホ横 844×390 / タブレット 768×1024・1024×768。
  `scrollWidth/Height > innerWidth/Height`（はみ出し）が無いこと、手持ちブロックが画面内で掴めることを確認。
- favicon の404、`apple-mobile-web-app-capable` の非推奨warningは**無害**。

## レスポンシブの要点（学習済み）
- 盤やコマのサイズは**「幅予算」と「高さ予算」の小さい方**で決める。横向きは高さがボトルネック。
- `resize`/`orientationchange` で**ゲーム状態を壊さず**再レイアウト（150msデバウンス）。セルサイズと手持ちコマ要素をその場で作り直す。
- 横向き省スペース用の `@media` は**スタイルシートの末尾**に置く。
  CSSの落とし穴: 同詳細度ルールはソース順で決まるため、上書きしたい基本ルールより**後ろ**に置かないと、後で定義されたセレクタには効かず黙って失敗する。

## canvas の おとしあな（学習済み）
- **flex の中の canvas は `min-width:0; min-height:0;` を必ず付ける**。付けないと canvas の内在サイズ（`width/height` 属性＝バックバッファ）が `min-width:auto` として効き、要素が巨大化して画面外へはみ出す（描いた線が見えない／座標がズレる）。`draw`・`coloring` で発生して修正済み。
- バックバッファは `CSSサイズ × min(devicePixelRatio,2)` にして、座標は `(clientX-rect.left)/rect.width*バッファ幅` で写す（くっきり＆ズレなし）。
- 入力は **Pointer Events（`pointerdown/move/up` ＋ `setPointerCapture`）** が単純で確実（タッチ＆マウス兼用、マルチタッチもID別に追える）。

## 画像の保存（iPhone/iPad 対応）⚠️必須パターン
**iOS Safari は `<a download>` を無視する**（写真に保存されず画像が開くだけ）。保存機能は次の3段で実装する（`draw`・`coloring` 実装済み）:
1. **Web Share**: `navigator.canShare({files:[file]})` が真なら `navigator.share({files})` → iOSの共有シートから「写真に保存」。
2. **PC**: それ以外で `download` 対応かつ非iOSなら `<a download>` でダウンロード。
3. **フォールバック**: 上記不可（古いiOS等）は、画像を全面オーバーレイで表示し「ながおしで しゃしんに ほぞん」を案内。
- 元データは `canvas.toBlob(...)`（無ければ `toDataURL`→`fetch`→`blob`）。iOS判定は `/(iPhone|iPad|iPod)/` ＋ `navigator.platform==="MacIntel"&&maxTouchPoints>1`（iPadOS）。

## ぬりえ（線画ぬり）エンジン（coloring）
- レイヤー分離：**線レイヤー**（黒・透明線）＋**ぬりレイヤー**（白背景）。表示は `ぬり→線` の順で重ね、線は常にくっきり。
- **バケツ＝フラッドフィル**（スキャンライン）。`線レイヤーの不透明ピクセルを“壁”`にして領域内だけ塗る。色一致は許容差つき。
- 線画は2種類対応：ベクター（`draw(g,S)` で閉じた領域を stroke）／**画像**（PNGの暗いピクセルだけを線として取り込み＝白背景は塗れる）。縦横比は線画に合わせる。
- 線画を増やすには `PICS` に1行：ベクターは `{emoji,name,ratio:1,draw}`、画像は `{emoji,name,src:"lines/xxx.png"}`（`sips -Z 900` 程度に縮小）。サムネイル一覧に自動で並ぶ。

## ぬりえ線画の作りかた（imagegen/ ・要対話ログイン）
- ローカルの `imagegen/`（gitignore）に AI画像生成ツールキットがある（genspark.ai をブラウザ自動操作、モデル「GPT Image 2」）。`prompts.txt`（塗り絵50枚・線画指定済み）→ `images/` に保存。
- **Claude は自走で生成できない**：`node save-session.js` が実Chromeでの**手動ログイン**必須のため。ユーザーが `save-session.js`→`generate.js` を実行する。手順は `imagegen/README.md`。
- 生成後の取り込みは Claude がやる：`sips -Z 900 imagegen/images/NNN_slug.png --out games/coloring/lines/slug.png` → `coloring` の `PICS` に `{emoji,name,src}` を追加。画像が十分そろったらベクター線画は削除可。

## そざい（線画・画像）の著作権ポリシー ⚠️
- 公開サイトに載せる素材は **自作 / 生成AIのオリジナル / CC0・パブリックドメイン** のみ。
- **第三者IPは不可**（例：ポケモン等の公式ぬりえ。「家庭で印刷OK」でも別サイトへの転載・ホスティングは許可されていない）。見た目が無料でも転載しない。
- 生成AIの線画は、特定キャラを模さない汎用モチーフにする。元の大きい画像は `.gitignore` に入れ、Web用縮小版だけ公開（例 `coloring/lines/dino.png`）。
- **フォントを同梱する場合**は OFL/CC0 等の再配布可ライセンスのみ。ライセンス全文を必ず同梱し、必要文字だけにサブセット化して軽量化する（例 `hiragana` のおてほん＝Klee One を OFL のままひらがなだけに絞り `font/kyokasho.woff2`＋`font/OFL.txt`、16KB）。

## ひらがな おてほんフォント（hiragana の学習）
- 教科書体（とめ・はね・はらいが出る）は iPhone/iPad に標準搭載されていない。OSフォント任せだと iOS では明朝に落ちる。
- 全端末で教科書体にするには **OFLフォントを必要字だけサブセットして同梱**する：`pyftsubset src.ttf --unicodes="3041-3096,..." --flavor=woff2 --no-hinting` → 十数KB。`@font-face` の家名は元と変えてOK（Reserved Font Name 回避）、`OFL.txt` を同梱。
- **canvas はフォントの読み込みを待たない**。`document.fonts.load(...).then(render)` ＋ `document.fonts.ready.then(render)` で、読めたら描き直す。

## リアルタイム物理（airhockey の学習）
- パドル等で動く物体が**壁とパドルの間に挟まって停止**しやすい。対策：①衝突時に必ず外向きの最低速度を与える ②**位置ベースの“はまり検知”**（速度ではなく、同じ場所に一定時間留まったら中央へ逃がす）③AIが角に張り付かないよう追従範囲を内側に制限。

## 最小SEO（ゲーム追加時に必ず付ける）
方針は「**title / description / canonical / OGP だけ**の軽量SEO」。
**トラッキング・広告・GA・外部スクリプトは入れない**（子供向け規制 COPPA/GDPR-K の回避＋静的・プライバシー優位の維持）。
- **公開URLの基点**: `https://haruharu20190701.github.io/kids-games/`
  （`<slug>` ゲームは `…/kids-games/games/<slug>/`。末尾スラッシュ付きの正規URLを使う）
- **OG画像**は全ページ共通で `…/kids-games/icon-1024.png`（絶対URL）。OGP は絶対URL必須。
- 各ゲームの `<head>`（`<title>` のところ）に貼るテンプレ（`<slug>`・なまえ・説明を置き換え）:
  ```html
  <title>＜なまえ＞｜こどもあそびば</title>
  <meta name="description" content="5さいくらいの こども向けの ＜どんなあそびか＞。むりょう・とうろくふよう・スマホ対応。" />
  <link rel="canonical" href="https://haruharu20190701.github.io/kids-games/games/<slug>/" />
  <!-- OGP（SNSシェアじの みため用）-->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="こどもあそびば" />
  <meta property="og:title" content="＜なまえ＞｜こどもあそびば" />
  <meta property="og:description" content="5さいくらいの こども向けの ＜どんなあそびか＞。" />
  <meta property="og:url" content="https://haruharu20190701.github.io/kids-games/games/<slug>/" />
  <meta property="og:image" content="https://haruharu20190701.github.io/kids-games/icon-1024.png" />
  <meta property="og:locale" content="ja_JP" />
  <meta name="twitter:card" content="summary" />
  ```
- `sitemap.xml` に足すブロック:
  ```xml
  <url>
    <loc>https://haruharu20190701.github.io/kids-games/games/<slug>/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  ```
- 確認（HTTP配信で）: `curl -s http://localhost:8000/games/<slug>/ | grep -iE '<title>|description|canonical|og:url'`。
  全URLが `200`、メニュー登録と sitemap の URL数が一致すること。
- OG画像は現状 正方形（1024px）を流用。将来 横長1200×630 に差し替えるとSNSカードがより映える（任意）。

## 公開フロー（GitHub Pages）
- main ブランチのルートで設定済み。デプロイは:
  `git add -A && git commit -m "..." && git push` → 約1〜3分で反映。
- gh のアクティブアカウントは **haruharu20190701**（必要なら `gh auth switch --user haruharu20190701`）。
- `.claude/`（ローカル設定・メモリ）は **.gitignore 済み。絶対に公開しない**。
- 相対パス（`../../index.html` など）のみ使用しているので、`/kids-games/` のサブパス配信でもそのまま動く。

### push が 403 になるとき（複数アカウント問題）
このマシンには gh アカウントが2つある（`fcyyamaguchi` と `haruharu20190701`）。
macOS のキーチェーンが旧アカウント `fcyyamaguchi` の資格情報を返し、
`git push` が `Permission ... denied to fcyyamaguchi` (403) になることがある。
その場合は、アクティブな haruharu のトークンで**資格情報ヘルパを介さず直接プッシュ**する:
```bash
gh auth switch --user haruharu20190701
git push "https://x-access-token:$(gh auth token)@github.com/haruharu20190701/kids-games.git" main
```
（トークンは一回限りのURLで使うだけ。表示・保存しないこと。
 この方法だと `origin/main` の追跡参照は更新されないので、必要なら後で `git fetch origin`。）

## コミットメッセージ
末尾に `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` を付ける（履歴参照）。
