# 品質管理共通ルール

## 🎯 目的
全プロジェクト共通の品質管理基準を定義し、一貫した高品質な開発を実現する。

## 📋 基本原則

### 最優先原則：「理解に追いつける範囲で進める」
```
人間の理解速度 > AI の生成速度
```

この原則により：
- ✅ コードの品質が保たれる
- ✅ 属人化を防げる
- ✅ 長期的なメンテナンス性が保たれる
- ✅ バグの早期発見が可能
- ✅ セキュリティリスクを低減

## 🎨 コード品質基準

### フォーマット・リント設定
```bash
# 共通設定
black src/ tests/ --line-length=88
flake8 src/ tests/ --max-line-length=120 --extend-ignore=E203,W503
mypy src/ --strict
```

### 品質設定ファイル

#### `.flake8`
```ini
[flake8]
max-line-length = 120
extend-ignore = E203, W503
exclude = .git,__pycache__,build,dist,venv
```

#### `mypy.ini`
```ini
[mypy]
python_version = 3.10
strict = True
warn_return_any = True
warn_unused_ignores = True
```

#### `pyproject.toml`
```toml
[tool.black]
line-length = 88
target-version = ['py310']

[tool.pytest.ini_options]
testpaths = ["tests"]
python_paths = ["src"]
```

### コミット前チェック
1. テスト実行
2. カバレッジ確認
3. フォーマット適用
4. 型チェック

## 📝 コミットメッセージ規約

### フォーマット
```
<type>: <subject>

<body>
```

### Type一覧
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `style`: フォーマット
- `refactor`: リファクタリング
- `test`: テスト追加・修正
- `chore`: その他

### 例
```
feat: 通知システムにSlack対応を追加

MessageFormatterクラスにSlack用のフォーマット機能を実装。
静かで簡潔なメッセージ生成を実現。
```

## 🏗️ プロジェクト構造標準

### 標準ディレクトリ構成
```
PROJECT_NAME/
├── src/PROJECT_NAME/       # コアモジュール
├── tests/                  # テストコード
├── docs/                   # ドキュメント
├── config/                 # 設定サンプル
├── scripts/                # 実行スクリプト
├── .kiro/                  # Kiro設定
│   ├── specs/              # 仕様書
│   └── steering/           # ステアリングルール
├── README.md               # プロジェクト概要
├── requirements.txt        # 依存関係
├── requirements-dev.txt    # 開発依存関係
├── setup.py               # パッケージ設定
└── pytest.ini            # テスト設定
```

## 📚 ドキュメント標準

### 必須ドキュメント
- `README.md`: プロジェクト概要（日英両対応）
- `CHANGELOG.md`: 変更履歴
- `docs/PROJECT_STRUCTURE.md`: プロジェクト構造
- `.kiro/specs/`: 仕様書（YAML形式）

### README構成
1. プロジェクト名と概要
2. バッジ（ライセンス、Python版数、テスト状況）
3. 言語選択（日本語・英語）
4. クイックスタート
5. 詳細ドキュメントへのリンク

## 🔄 CI/CD標準

### GitHub Actions テンプレート
```yaml
name: Tests

on:
  push:
    branches: [main, 'feature/**', 'bugfix/**']
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run tests
        run: pytest tests/ -v
      
      - name: Check coverage
        run: pytest --cov=src --cov-report=html
      
      - name: Lint
        run: |
          black --check src/ tests/
          flake8 src/ tests/
```

## 🎯 適用プロジェクト

- ✅ Komon
- ✅ Okina
- 🔄 今後の新プロジェクト全て