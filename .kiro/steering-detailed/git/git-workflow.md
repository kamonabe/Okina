# Git運用共通ルール

## 🎯 基本方針

全プロジェクトで**mainブランチを絶対に壊さない**ことを最優先とします。

## 🌿 Gitブランチ戦略

### mainブランチで作業してOK

以下の作業は**mainブランチで直接**行います：

- ドキュメント整備（README, CHANGELOG等）
- future-ideas.mdへのアイデア追加
- implementation-tasks.mdへのタスク追加
- Spec作成（requirements.yml, design.yml, tasks.yml）
- ステアリングルールの追加・更新

### 開発ブランチを切る必要がある

以下の作業は**必ず開発ブランチ**を作成してから行います：

- **コード実装**（src/配下の変更）
- **テスト追加**（tests/配下の変更）
- **設定ファイル変更**（settings.yml, setup.py等）
- **依存パッケージ変更**（requirements.txt等）

### ブランチ命名規則

```
feature/task-XXX-{feature-name}     # 新機能
bugfix/{issue-description}          # バグ修正
refactor/{module-name}              # リファクタリング

例:
- feature/task-001-progressive-notification
- feature/task-003-contextual-advice
- bugfix/fix-memory-leak
- refactor/analyzer-module
```

## 🛡️ Git運用の安全策

### 前提条件チェック

#### .gitの存在確認

プロジェクト内に `.git` が存在しない場合：
- Git関連の処理は実行しない
- 代わりに次のような**推奨コメント**を表示

```
現在このプロジェクトにはGitが設定されていません。
Gitを導入するとバージョン管理や安全な開発フローが利用できるため推奨です。
```

- Git導入の判断は開発者に委ねる（強制しない）
- 希望する場合は、自動化フローを提供：
  - `git init`
  - `.gitignore` 自動生成
  - GitHub/社内Gitへのリポジトリ作成
  - mainブランチの作成
  - 初期commit/pushの案内

### 作業開始前の必須手順

**新しい作業ブランチを切る前に、必ず origin/main と同期する**

これは**複数マシン開発**や**チーム開発**で、以下の事故を防ぐための保険：
- 古いmainから作業を開始してしまう
- 他の人の変更を知らずに開発してしまう
- マージ時に余計なコンフリクトが発生する

#### 手順

```bash
# 1. リモート情報を最新化
git fetch origin

# 2. mainに移動
git switch main

# 3. origin/mainを取り込む
git pull origin main

# 4. 最新のmainからfeatureブランチを作成
git switch -c feature/task-XXX-{feature-name}
```

#### なぜ必要か

一人開発では気づきにくいが、以下の状況で必須になる：
- **複数マシンで開発**：PC-Aで作業 → push → PC-Bで作業開始時にpull忘れ
- **チーム開発**：他の人がmainにマージ → 自分は古いmainから作業
- **長期間の作業**：feature作業中にmainが進んでいる

### マージ前の安全確認（マージテスト）

**mainに直接マージする前に、仮マージで動作確認を行う**

#### 手順

```bash
# 1. 作業ブランチで最新のmainを取り込む
git switch feature/task-XXX-{feature-name}
git fetch origin
git merge origin/main

# 2. コンフリクトがあれば解決

# 3. テスト実行
pytest tests/ -v
pytest --cov=src --cov-report=term

# 4. 問題なければmainにマージ
git switch main
git merge feature/task-XXX-{feature-name}
git push origin main
```

## 🔧 Git設定

### 共通Git設定
```bash
git config --global user.name "kamonabe"
git config --global user.email "kamonabe1927@gmail.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
```

### .gitignore テンプレート
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.cache

# OS
.DS_Store
Thumbs.db

# Project specific
test-results/
```

## 🚨 実装開始前の必須チェック

**⚠️ 重要**: このチェックをスキップするとmainブランチが破壊される危険性があります。

**実装を開始する前に、必ず以下を厳格に実行**：

### ステップ1: 環境の安全性確認
```bash
# 1. 現在のブランチを確認（必須）
git branch

# 2. 作業ディレクトリの状態確認
git status

# 3. システム時刻の確認（コミット時刻の正確性のため）
date
```

### ステップ2: ブランチ安全性の判定
- ✅ **開発ブランチにいる場合**: 実装を開始
- ❌ **mainブランチにいる場合**: **即座に停止**

### ステップ3: mainブランチの場合の対応
**以下を必ず実行**：

1. **実装を開始しない**（コード変更を一切行わない）
2. **明確な警告を表示**：
   ```
   🚨 危険: mainブランチで実装しようとしています
   
   【リスク】
   - mainブランチの破壊
   - 他の開発者への影響
   - リリース品質の低下
   
   【必要な作業】
   開発ブランチを作成してください：
   
   git checkout -b feature/task-XXX-{feature-name}
   
   ブランチ作成後、「ブランチ作成完了」とお知らせください。
   ```
3. **ユーザーの返答を待機**（実装は開始しない）

## 🎯 適用プロジェクト

- ✅ Komon
- ✅ Okina
- 🔄 今後の新プロジェクト全て