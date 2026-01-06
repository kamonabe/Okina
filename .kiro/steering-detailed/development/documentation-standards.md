# ドキュメント標準ガイド

## 🎯 目的
全プロジェクト共通のドキュメント作成標準を定義し、
一貫性があり保守しやすいドキュメントを実現する。

## 📚 必須ドキュメント

### プロジェクトレベル
```
PROJECT_NAME/
├── README.md                   # プロジェクト概要（日英両対応）
├── CHANGELOG.md               # 変更履歴
├── LICENSE                     # ライセンス
├── CONTRIBUTING.md            # 貢献ガイド
└── CODE_OF_CONDUCT.md         # 行動規範
```

### 技術ドキュメント
```
docs/
├── PROJECT_STRUCTURE.md       # プロジェクト構造
├── INSTALLATION.md            # インストールガイド
├── CONFIGURATION.md           # 設定ガイド
├── API_REFERENCE.md           # API仕様
├── TROUBLESHOOTING.md         # トラブルシューティング
└── DEVELOPMENT.md             # 開発者ガイド
```

## 📝 README.md 標準構成

### 基本テンプレート
```markdown
# プロジェクト名

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Tests](https://github.com/kamonabe/PROJECT_NAME/workflows/Tests/badge.svg)](https://github.com/kamonabe/PROJECT_NAME/actions)
[![Coverage](https://codecov.io/gh/kamonabe/PROJECT_NAME/branch/main/graph/badge.svg)](https://codecov.io/gh/kamonabe/PROJECT_NAME)

## 言語選択 / Language Selection

- [日本語](#日本語版) 
- [English](#english-version)

---

## 日本語版

### 概要

プロジェクトの簡潔な説明（1-2文）

### 特徴

- 🎯 主要機能1
- 🚀 主要機能2  
- 🛡️ 主要機能3

### クイックスタート

```bash
# インストール
pip install PROJECT_NAME

# 基本的な使用例
PROJECT_NAME --help
```

### ドキュメント

- [インストールガイド](docs/INSTALLATION.md)
- [設定ガイド](docs/CONFIGURATION.md)
- [API仕様](docs/API_REFERENCE.md)
- [トラブルシューティング](docs/TROUBLESHOOTING.md)

### ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

---

## English Version

### Overview

Brief project description (1-2 sentences)

### Features

- 🎯 Key feature 1
- 🚀 Key feature 2
- 🛡️ Key feature 3

### Quick Start

```bash
# Installation
pip install PROJECT_NAME

# Basic usage
PROJECT_NAME --help
```

### Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [API Reference](docs/API_REFERENCE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

### License

MIT License - see [LICENSE](LICENSE) for details
```

## 📋 CHANGELOG.md 標準

### フォーマット
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 新機能の説明

### Changed
- 変更された機能の説明

### Deprecated
- 非推奨になった機能の説明

### Removed
- 削除された機能の説明

### Fixed
- 修正されたバグの説明

### Security
- セキュリティ関連の変更

## [1.0.0] - 2025-01-06

### Added
- 初回リリース
- 基本機能の実装

[Unreleased]: https://github.com/kamonabe/PROJECT_NAME/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/kamonabe/PROJECT_NAME/releases/tag/v1.0.0
```

## 🔧 API仕様ドキュメント

### docstring標準
```python
def send_notification(message: str, channel: str = "#general") -> bool:
    """通知を送信する
    
    Args:
        message (str): 送信するメッセージ
        channel (str, optional): 送信先チャンネル. Defaults to "#general".
    
    Returns:
        bool: 送信成功時True、失敗時False
    
    Raises:
        ValueError: メッセージが空の場合
        ConnectionError: 通信エラーの場合
    
    Example:
        >>> send_notification("テストメッセージ", "#alerts")
        True
        
        >>> send_notification("", "#alerts")
        ValueError: メッセージが空です
    """
    if not message.strip():
        raise ValueError("メッセージが空です")
    
    try:
        # 実装
        return True
    except Exception as e:
        raise ConnectionError(f"通信エラー: {e}")
```

### クラスドキュメント
```python
class NotificationManager:
    """通知管理クラス
    
    複数の通知プラットフォームを統合管理し、
    一貫したインターフェースで通知送信を行う。
    
    Attributes:
        platforms (List[str]): 対応プラットフォーム一覧
        default_channel (str): デフォルト送信先
    
    Example:
        >>> manager = NotificationManager()
        >>> manager.send("メッセージ", "slack")
        True
    """
    
    def __init__(self, config: Dict[str, Any]):
        """初期化
        
        Args:
            config (Dict[str, Any]): 設定辞書
                - slack_webhook: SlackのWebhook URL
                - discord_webhook: DiscordのWebhook URL
        """
        pass
```

## 📖 ユーザーガイド標準

### インストールガイド構成
```markdown
# インストールガイド

## システム要件

- Python 3.10以上
- pip 21.0以上
- OS: Linux, macOS, Windows

## インストール方法

### PyPIからのインストール（推奨）

```bash
pip install PROJECT_NAME
```

### ソースからのインストール

```bash
git clone https://github.com/kamonabe/PROJECT_NAME.git
cd PROJECT_NAME
pip install -e .
```

### 開発環境のセットアップ

```bash
git clone https://github.com/kamonabe/PROJECT_NAME.git
cd PROJECT_NAME
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements-dev.txt
```

## インストール確認

```bash
PROJECT_NAME --version
```

## トラブルシューティング

### よくある問題

#### Python バージョンエラー
```
ERROR: Python 3.9 is not supported
```

**解決方法**: Python 3.10以上をインストールしてください。
```

## 🧪 コードサンプル標準

### 基本的な使用例
```python
# examples/basic_usage.py
"""基本的な使用例"""

from PROJECT_NAME import MainClass

def main():
    """メイン処理"""
    # 初期化
    instance = MainClass(config="config/settings.yml")
    
    # 基本操作
    result = instance.process("input_data")
    print(f"結果: {result}")

if __name__ == "__main__":
    main()
```

### 高度な使用例
```python
# examples/advanced_usage.py
"""高度な使用例"""

from PROJECT_NAME import MainClass, CustomHandler

def advanced_example():
    """高度な使用例"""
    # カスタムハンドラーを使用
    handler = CustomHandler(
        on_success=lambda x: print(f"成功: {x}"),
        on_error=lambda e: print(f"エラー: {e}")
    )
    
    # 設定をカスタマイズ
    instance = MainClass(
        config="config/advanced.yml",
        handler=handler,
        debug=True
    )
    
    # バッチ処理
    results = instance.batch_process([
        "data1", "data2", "data3"
    ])
    
    return results

if __name__ == "__main__":
    results = advanced_example()
    print(f"処理結果: {len(results)}件")
```

## 📋 ドキュメント品質チェックリスト

### 作成時
- [ ] 目的が明確に記載されている
- [ ] 対象読者が明確
- [ ] 手順が具体的で実行可能
- [ ] コードサンプルが動作する
- [ ] 日本語の文法・表記が正しい

### レビュー時
- [ ] 情報が最新である
- [ ] リンクが有効である
- [ ] 画像・図表が適切
- [ ] 誤字・脱字がない
- [ ] 一貫性がある

### 更新時
- [ ] 変更内容をCHANGELOG.mdに記録
- [ ] 関連ドキュメントも更新
- [ ] バージョン情報を更新
- [ ] 古い情報を削除

## 🎨 マークダウン記法標準

### 見出し
```markdown
# レベル1（ページタイトル）
## レベル2（主要セクション）
### レベル3（サブセクション）
#### レベル4（詳細項目）
```

### 強調・装飾
```markdown
**太字** - 重要な用語
*斜体* - 英語用語
`コード` - コマンド・ファイル名
```

### リスト
```markdown
# 順序なしリスト
- 項目1
- 項目2
  - サブ項目

# 順序ありリスト
1. 手順1
2. 手順2
   1. サブ手順
```

### コードブロック
```markdown
```python
# Python コード
def example():
    return "Hello"
```

```bash
# シェルコマンド
pip install package
```
```

## 🎯 適用プロジェクト

- ✅ Komon
- ✅ Okina
- 🔄 今後の新プロジェクト全て

---

**最終更新**: 2025-01-06
**重要度**: 高（ドキュメント品質）