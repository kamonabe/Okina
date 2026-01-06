# プロジェクト構造標準ガイド

## 🎯 目的
全プロジェクト共通の標準的なディレクトリ構造を定義し、
一貫性のある保守しやすいプロジェクト構成を実現する。

## 📁 標準ディレクトリ構成

### 基本構造
```
PROJECT_NAME/
├── src/PROJECT_NAME/           # コアモジュール
│   ├── __init__.py
│   ├── core/                   # 核となる機能
│   ├── utils/                  # ユーティリティ
│   ├── config/                 # 設定管理
│   └── exceptions.py           # カスタム例外
├── tests/                      # テストコード
│   ├── unit/                   # ユニットテスト
│   ├── integration/            # 統合テスト
│   ├── property/               # プロパティテスト
│   └── conftest.py            # pytest設定
├── docs/                       # ドキュメント
│   ├── api/                    # API仕様
│   ├── user-guide/             # ユーザーガイド
│   └── development/            # 開発者向け
├── config/                     # 設定サンプル
│   ├── settings.yml.example
│   └── logging.yml
├── scripts/                    # 実行スクリプト
│   ├── setup.py               # セットアップ
│   ├── validate.py            # 検証
│   └── release.py             # リリース
├── .kiro/                      # Kiro設定
│   ├── specs/                  # 仕様書
│   └── steering/               # ステアリングルール
├── .github/                    # GitHub設定
│   └── workflows/              # CI/CD
├── data/                       # データファイル
│   ├── input/                  # 入力データ
│   └── output/                 # 出力データ
├── README.md                   # プロジェクト概要
├── CHANGELOG.md               # 変更履歴
├── LICENSE                     # ライセンス
├── requirements.txt            # 依存関係
├── requirements-dev.txt        # 開発依存関係
├── setup.py                   # パッケージ設定
├── pytest.ini                # テスト設定
├── .gitignore                 # Git除外設定
└── version.txt                # バージョン管理
```

## 📦 src/ ディレクトリ設計

### モジュール分割原則
```python
src/PROJECT_NAME/
├── __init__.py                 # パッケージ初期化
├── core/                       # 核となるビジネスロジック
│   ├── __init__.py
│   ├── engine.py              # メインエンジン
│   └── processor.py           # 処理ロジック
├── models/                     # データモデル
│   ├── __init__.py
│   ├── base.py                # 基底クラス
│   └── entities.py            # エンティティ
├── services/                   # サービス層
│   ├── __init__.py
│   └── notification.py        # 通知サービス
├── utils/                      # ユーティリティ
│   ├── __init__.py
│   ├── helpers.py             # ヘルパー関数
│   └── validators.py          # 検証機能
├── config/                     # 設定管理
│   ├── __init__.py
│   ├── settings.py            # 設定読み込み
│   └── constants.py           # 定数定義
└── exceptions.py              # カスタム例外
```

### 命名規約
```python
# ファイル名：snake_case
notification_manager.py
message_formatter.py

# クラス名：PascalCase
class NotificationManager:
class MessageFormatter:

# 関数名：snake_case
def send_notification():
def format_message():

# 定数：UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
```

## 🧪 tests/ ディレクトリ設計

### テスト分類
```
tests/
├── unit/                       # ユニットテスト
│   ├── test_core.py           # core モジュール
│   ├── test_services.py       # services モジュール
│   └── test_utils.py          # utils モジュール
├── integration/                # 統合テスト
│   ├── test_notification_flow.py
│   └── test_end_to_end.py
├── property/                   # プロパティテスト
│   ├── test_message_properties.py
│   └── test_data_consistency.py
├── fixtures/                   # テストデータ
│   ├── sample_data.json
│   └── mock_responses.py
└── conftest.py                # pytest共通設定
```

### テストファイル命名
```python
# テストファイル：test_*.py
test_notification_manager.py
test_message_formatter.py

# テストクラス：Test*
class TestNotificationManager:
class TestMessageFormatter:

# テストメソッド：test_*
def test_send_notification_success():
def test_format_message_with_changes():
```

## 📚 docs/ ディレクトリ設計

### ドキュメント構造
```
docs/
├── README.md                   # ドキュメント概要
├── api/                        # API仕様
│   ├── core.md                # コアAPI
│   └── services.md            # サービスAPI
├── user-guide/                 # ユーザーガイド
│   ├── installation.md        # インストール
│   ├── quick-start.md         # クイックスタート
│   └── configuration.md       # 設定方法
├── development/                # 開発者向け
│   ├── setup.md               # 開発環境構築
│   ├── testing.md             # テスト実行
│   └── contributing.md        # 貢献ガイド
└── examples/                   # 使用例
    ├── basic-usage.py
    └── advanced-usage.py
```

## ⚙️ 設定ファイル標準

### 必須設定ファイル
```yaml
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --strict-markers --disable-warnings

# .gitignore
__pycache__/
*.py[cod]
*$py.class
.env
.env.local
*.log
.coverage
htmlcov/
dist/
build/
*.egg-info/

# requirements.txt（本番用）
# 必要最小限の依存関係
requests>=2.28.0,<3.0.0
pyyaml>=6.0,<7.0

# requirements-dev.txt（開発用）
-r requirements.txt
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
```

## 🔧 scripts/ ディレクトリ設計

### 標準スクリプト
```python
scripts/
├── setup.py                   # 開発環境セットアップ
├── validate.py                # コード品質検証
├── test.py                    # テスト実行
├── build.py                   # ビルド処理
├── release.py                 # リリース処理
└── clean.py                   # クリーンアップ
```

### スクリプト例
```python
# scripts/validate.py
#!/usr/bin/env python3
"""コード品質検証スクリプト"""

import subprocess
import sys

def run_command(cmd: str) -> bool:
    """コマンド実行"""
    print(f"実行中: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    """メイン処理"""
    checks = [
        "black --check src/ tests/",
        "flake8 src/ tests/",
        "mypy src/",
        "pytest tests/ --cov=src"
    ]
    
    for check in checks:
        if not run_command(check):
            print(f"❌ 失敗: {check}")
            sys.exit(1)
    
    print("✅ 全ての品質チェックが成功しました")

if __name__ == "__main__":
    main()
```

## 📋 プロジェクト作成チェックリスト

### 初期セットアップ
- [ ] ディレクトリ構造作成
- [ ] 必須ファイル作成（README.md, LICENSE, .gitignore）
- [ ] 設定ファイル作成（pytest.ini, requirements.txt）
- [ ] パッケージ初期化（__init__.py）

### 開発環境
- [ ] 仮想環境作成
- [ ] 依存関係インストール
- [ ] Git初期化
- [ ] CI/CD設定

### 品質管理
- [ ] テスト環境構築
- [ ] コード品質ツール設定
- [ ] pre-commitフック設定
- [ ] カバレッジ測定設定

## 🎯 プロジェクト固有カスタマイズ

### Komon固有
```
src/komon/
├── core/
│   ├── engine.py              # Komonエンジン
│   └── processor.py           # 処理ロジック
├── models/
│   └── task.py                # タスクモデル
└── services/
    └── task_manager.py        # タスク管理
```

### Okina固有
```
src/okina/
├── core/
│   ├── change_monitor.py      # 変化監視
│   └── diff_analyzer.py       # 差分抽出
├── models/
│   └── change.py              # 変化モデル
└── services/
    └── notification.py        # 通知サービス
```

## 🎯 適用プロジェクト

- ✅ Komon
- ✅ Okina
- 🔄 今後の新プロジェクト全て

---

**最終更新**: 2025-01-06
**重要度**: 高（構造標準化）