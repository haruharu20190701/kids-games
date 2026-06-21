# こどもあそびば 🎈

子供向けのゲームや教育に使える Web アプリを集めたディレクトリです。
すべて **HTML/CSS/JS の単一ファイル完結・外部ライブラリ不要**で作り、ブラウザで開くだけで動きます。

## フォルダ構成

```
kids/
├── index.html              ゲーム選択メニュー（ランチャー）
├── games/                  ゲーム本体。1ゲーム＝1フォルダ＝index.html
│   ├── puzzle-block/        🧩 ぱずるぶろっく（ステージ制パズル）
│   ├── piano/              🎹 ぴあの（自由演奏＋おてほん曲）
│   ├── draw/               🎨 おえかき（自由描画・スタンプ）
│   ├── memory/             🃏 しんけいすいじゃく（神経衰弱）
│   ├── numbers/            🔢 かずあそび（数を数える）
│   ├── airhockey/          🏒 エアホッケー（CPU/2人）
│   └── coloring/           🖍️ ぬりえ（バケツ塗り・lines/ に線画）
├── shared/                 複数ゲームで共通利用するCSS/JS（任意）
├── robots.txt / sitemap.xml  検索エンジン向け（ゲーム追加時に sitemap を更新）
└── README.md
```

## あそびかた

`index.html` をブラウザで開く → 遊びたいゲームを選ぶ。

ローカルサーバーで開く場合（推奨）:

```bash
python3 -m http.server 8000
# → http://localhost:8000 を開く
```

## 新しいゲームの追加手順

1. `games/<ゲーム名>/index.html` を作る（ゲーム名は半角英数のスラッグ推奨。例: `numbers`, `memory-card`）。
2. メニューに載せる。`index.html` の `GAMES` 配列に1行足すだけ:

   ```js
   { name:"すうじあそび", emoji:"🔢", path:"games/numbers/index.html" },
   ```

   - `soon:true` を付けると「じゅんびちゅう」表示（クリック不可）になります。
3. **最小SEOを付ける**：新ページの `<head>` に `title` / `description` / `canonical` / OGP を入れ、`sitemap.xml` に新URLを1ブロック追記する（メニュー登録と sitemap は必ず一致させる）。テンプレと詳細は `CLAUDE.md`「最小SEO」を参照。
   - トラッキング・広告・外部スクリプトは入れない方針（軽量・プライバシー優先）。

## 制作の方針（5歳前後むけ）

- 時間制限なし・失敗にやさしい・「できた！」が気持ちいい演出
- ひらがな中心の表示、大きなタップ領域、タッチ＆マウス両対応
- 効果音は Web Audio API で生成（音声ファイル不要＝軽量）
