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
│   ├── puzzle-block/        ぱずるぶろっく
│   └── piano/              ぴあの
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
