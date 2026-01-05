# Okina（翁）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)](https://www.linux.org/)

---

## 🌏 Language / 言語

- **[日本語版](#日本語版)** ⬇️ このまま下にスクロール
- **[English Version](#english-version)** ⬇️ Scroll down to English section

---

# 日本語版

**Okina は、ファームウェア・ソフトウェア更新の変化を静かに見守る変化検知ツールです。**

ネットワーク機器や基盤ソフトウェアのファームウェア更新において「気づかなかった」による事故を減らすための補助的・保険的な仕組みとして設計されています。

🏮 Okina は縁側に座って世界を見ている翁のような存在です。静かに見守り、前と違えば知らせ、判断は人に委ねます。

---

## 📖 目次

- [なぜOkinaなのか？](#-なぜokinaなのか)
- [このような結果が得られます](#-このような結果が得られます)
- [設計哲学](#-設計哲学重要)
- [全体構造](#-全体構造責務分離)
- [クイックスタート](#-クイックスタート所要時間-約10分)
- [コマンドリファレンス](#-コマンドリファレンス)
- [設定](#️-設定)
- [定期実行](#-定期実行cron)
- [Input Provider の作成](#-input-provider-の作成)
- [ドキュメント](#-ドキュメント)
- [開発](#-開発)
- [対応プラットフォーム](#-対応プラットフォーム)
- [FAQ](#-faq)
- [コントリビューション](#-コントリビューション)
- [ライセンス](#-ライセンス)

---

## 🤔 なぜOkinaなのか？

### 現実的に発生しうる事故

ネットワーク機器や基盤ソフトウェアのファームウェア更新において、以下のような事故が現実的に発生します：

1. ベンダーから新ファームウェアが公開された
2. 技術担当がその事実に気づかなかった
3. 自動アップデート、または半自動更新が走った
4. 事前検証なしで環境に変更が入り、不具合が発生した

### 問題の本質

この事故の本質は「誰かが悪い」ではなく、**「人が"気づく"ことを前提にした構造」そのものにリスクがある**点にあります。

### Okinaの役割

Okinaは、この「気づかなかった」を減らすための**補助的・保険的な仕組み**として設計されています。

---

## 🎯 このような結果が得られます

`okina check` コマンドを実行すると、前回との差分を検出して通知します：

```bash
$ okina check

🔍 変化検知を実行中...

📊 検知結果
ソース: fortinet-docs
期間: 2025-12-21 → 2025-12-22

✨ 新規追加 (2件)
• FortiOS 7.6.7 Release Notes
  https://docs.fortinet.com/document/fortigate/7.6.7/fortios-release-notes
  
• FortiAnalyzer 7.4.5 Release Notes  
  https://docs.fortinet.com/document/fortianalyzer/7.4.5/release-notes

🔄 内容変更 (1件)
• FortiOS 7.6.6 Release Notes
  https://docs.fortinet.com/document/fortigate/7.6.6/fortios-release-notes
  変更: PDF URLが更新されました

📤 Slack通知を送信しました
```

### Slack通知例

```
🏮 Okina（翁）からのお知らせ

📅 2025-12-22 14:30:00
🔍 ソース: fortinet-docs

✨ 新規追加: 2件
🔄 内容変更: 1件

詳細は okina history で確認できます
```

---

## 🎭 設計哲学（重要）

Okinaの設計哲学を理解することが、適切な利用の前提条件です：

### 基本原則

- Okinaは **主役ではない**
- Okinaは **判断しない**  
- Okinaは **自動適用しない**
- Okinaは **人や運用を置き換えない**

### Okinaの役割

> **「いつもと違う」ことを静かに知らせること**

このツールに過剰な信頼や期待を持たせないことが、利用上の前提条件です。

### 翁のような存在

Okinaは縁側に座って世界を見ている翁のような存在です：
- 静かに見守る
- 前と違えば知らせる  
- 判断は人に委ねる
- 決して出しゃばらない

---

## 🏗 全体構造（責務分離）

Okinaは以下の処理フローの **③④⑤のみを担当**します：

```
① 取得（サイト依存）        ← Input Provider
② 正規化アウトプット生成     ← Input Provider  
    ↓
③ 変化検知                 ← Okina
④ 差分抽出                 ← Okina
⑤ 通知                    ← Okina
```

### Input Provider とは

①②を担当する外部プログラムです：
- Webサイトのクローリング
- HTML/PDFの解析  
- 正規化データ（JSON Lines）の生成

### Okina の責務

③④⑤のみに集中することで、シンプルで信頼性の高い動作を実現します：
- 前回との差分検出
- 変化があれば通知
- 取得失敗・異常も通知

---

## 🚀 クイックスタート（所要時間: 約10分）

### 1. インストール

```bash
# PyPIからインストール（将来対応予定）
pip install okina

# または、ソースからインストール
git clone https://github.com/kamonabe/Okina.git
cd Okina
pip install -e .
```

### 2. 設定ファイルの作成

```bash
# 設定ファイルのサンプルをコピー
cp config/settings.yml.sample settings.yml

# 設定を編集（Slack Webhook URLなど）
vim settings.yml
```

### 3. 環境変数の設定

```bash
# Slack Webhook URLを環境変数に設定
export OKINA_SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 4. Input Provider の準備

```bash
# データディレクトリを作成
mkdir -p data/input

# サンプルデータを配置（実際はInput Providerが生成）
cat > data/input/sample.jsonl << 'EOF'
{"schema": "okina.item.v1", "source": "sample", "id": "test:product:1.0.0:release", "type": "release", "title": "Test Product 1.0.0", "url": "https://example.com/1.0.0", "observed_at": "2025-12-22T10:00:00+09:00", "version": "1.0.0"}
EOF
```

### 5. 初回実行

```bash
# 設定検証
okina config validate

# 変化検知実行
okina check

# ステータス確認  
okina status
```

---

## 📋 コマンドリファレンス

### 基本コマンド

```bash
# 変化検知を実行
okina check

# ステータス表示
okina status

# 履歴表示
okina history

# 設定検証
okina config validate
```

### オプション

```bash
# 詳細出力
okina check --verbose

# 通知なしで実行（テスト用）
okina check --dry-run

# 特定のソースのみ処理
okina check --source fortinet-docs

# 履歴の件数指定
okina history --limit 20
```

---

## ⚙️ 設定

### 設定ファイル（settings.yml）

```yaml
profile:
  usage: "production"  # "production" または "dev"

input:
  data_directory: "data/input"
  file_pattern: "*.jsonl"
  
storage:
  history_directory: "data/history"
  max_history_days: 30

notifications:
  slack:
    enabled: true
    webhook_url: "env:OKINA_SLACK_WEBHOOK"
    channel: "#alerts"
    username: "Okina（翁）"
    icon_emoji: ":older_man:"

output:
  default_mode: "normal"
  max_items_per_notification: 10
```

### 環境変数

```bash
# 必須
export OKINA_SLACK_WEBHOOK="https://hooks.slack.com/services/..."

# オプション
export OKINA_DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."
export OKINA_EMAIL_PASSWORD="your-email-password"
```

---

## ⏰ 定期実行（cron）

### cron設定例

```bash
# 毎日朝9時に実行
0 9 * * * /usr/local/bin/okina check

# 平日の朝夕に実行  
0 9,18 * * 1-5 /usr/local/bin/okina check

# 毎時実行（必要な場合のみ）
0 * * * * /usr/local/bin/okina check
```

### systemd-timer設定例

```ini
# /etc/systemd/system/okina.service
[Unit]
Description=Okina Change Detection
After=network.target

[Service]
Type=oneshot
User=okina
WorkingDirectory=/opt/okina
ExecStart=/usr/local/bin/okina check
Environment=OKINA_SLACK_WEBHOOK=https://hooks.slack.com/services/...

# /etc/systemd/system/okina.timer  
[Unit]
Description=Run Okina daily
Requires=okina.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

---

## 🔌 Input Provider の作成

### 正規化データ仕様

Input Providerは以下の形式でデータを出力する必要があります：

#### フォーマット
- JSON Lines（`.jsonl`）
- 1行 = 1アイテム
- UTF-8エンコーディング

#### スキーマ（v1）
```json
{
  "schema": "okina.item.v1",
  "source": "fortinet-docs", 
  "id": "fortinet:fortios:7.6.6:release",
  "type": "release",
  "title": "FortiOS 7.6.6 Release Notes",
  "version": "7.6.6",
  "url": "https://docs.fortinet.com/...",
  "observed_at": "2025-12-22T14:30:00+09:00",
  "payload": {
    "major": "7.6",
    "pdf_url": "https://..."
  }
}
```

#### 必須フィールド
- `schema`: スキーマバージョン
- `source`: データソース識別子  
- `id`: 一意識別子
- `type`: アイテムタイプ
- `title`: 人間が読める名前
- `url`: 参照URL
- `observed_at`: 観測日時（ISO 8601）

#### ID設計ルール
- 同一の論理対象は常に同じID
- URL変更に極力影響されない
- 人間が見て意味が分かる

推奨形式：`vendor:product:version:type`

### Input Provider 実装例

```python
#!/usr/bin/env python3
"""
Fortinet ドキュメント用 Input Provider 例
"""
import json
import requests
from datetime import datetime
from pathlib import Path

def fetch_fortinet_releases():
    """Fortinetのリリース情報を取得"""
    # 実際の実装では適切なAPIやスクレイピングを行う
    releases = [
        {
            "version": "7.6.6",
            "title": "FortiOS 7.6.6 Release Notes",
            "url": "https://docs.fortinet.com/document/fortigate/7.6.6/fortios-release-notes",
            "pdf_url": "https://docs.fortinet.com/document/fortigate/7.6.6/fortios-release-notes/pdf"
        }
    ]
    
    # 正規化データに変換
    normalized = []
    for release in releases:
        item = {
            "schema": "okina.item.v1",
            "source": "fortinet-docs",
            "id": f"fortinet:fortios:{release['version']}:release",
            "type": "release", 
            "title": release["title"],
            "version": release["version"],
            "url": release["url"],
            "observed_at": datetime.now().isoformat(),
            "payload": {
                "major": ".".join(release["version"].split(".")[:2]),
                "pdf_url": release["pdf_url"]
            }
        }
        normalized.append(item)
    
    return normalized

def main():
    """メイン処理"""
    releases = fetch_fortinet_releases()
    
    # data/input/fortinet.jsonl に出力
    output_path = Path("data/input/fortinet.jsonl")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for item in releases:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"✅ {len(releases)} items written to {output_path}")

if __name__ == "__main__":
    main()
```

---

## 📚 ドキュメント

- [プロジェクト構造](docs/PROJECT_STRUCTURE.md)
- [コマンドリファレンス](docs/COMMAND_REFERENCE.md)
- [設定リファレンス](docs/CONFIGURATION.md)
- [Input Provider ガイド](docs/INPUT_PROVIDER_GUIDE.md)
- [運用ガイド](docs/OPERATIONS.md)
- [変更履歴](docs/CHANGELOG.md)

---

## 🛠 開発

### 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/kamonabe/Okina.git
cd Okina

# 開発用依存関係をインストール
pip install -r requirements-dev.txt

# 開発モードでインストール
pip install -e .
```

### テスト実行

```bash
# 全テスト実行
pytest tests/ -v

# カバレッジ測定
bash run_coverage.sh

# 特定のテストのみ実行
pytest tests/test_monitor.py -v
```

### コード品質チェック

```bash
# フォーマット
black src/ tests/

# リント
flake8 src/ tests/

# 型チェック
mypy src/
```

### 開発原則

- **「理解に追いつける範囲で進める」**: AI支援開発でも人間の理解を優先
- **テストカバレッジ90%以上**: 信頼性の確保
- **仕様駆動開発**: `.kiro/specs/` で仕様を管理

---

## 🖥 対応プラットフォーム

### 動作環境
- **OS**: Linux（推奨）
- **Python**: 3.10以上
- **アーキテクチャ**: x86_64, ARM64

### 検証済み環境
- AlmaLinux 9
- Ubuntu 22.04 LTS
- Rocky Linux 9
- Amazon Linux 2023

### 依存関係
- PyYAML >= 6.0
- requests >= 2.31.0

---

## ❓ FAQ

### Q: Okinaは何を監視しますか？
A: Okinaは直接的な監視は行いません。Input Providerが生成した正規化データの変化を検知します。

### Q: 自動アップデートは行いますか？
A: いいえ。Okinaは変化を通知するだけで、自動的な更新は一切行いません。

### Q: どのくらいの頻度で実行すべきですか？
A: 用途によりますが、1日1回〜毎時程度を推奨します。過度な頻度は避けてください。

### Q: Input Providerはどこで入手できますか？
A: 現在は各自で作成していただく必要があります。将来的にはサンプル集を提供予定です。

### Q: 通知が来ない場合は？
A: `okina status` でエラーログを確認し、設定ファイルとWebhook URLを検証してください。

### Q: 履歴データはどのくらい保持されますか？
A: デフォルトでは30日間です。`settings.yml` の `max_history_days` で変更可能です。

---

## 🤝 コントリビューション

Okinaプロジェクトへの貢献を歓迎します！

### 貢献方法

1. **Issue報告**: バグ報告や機能要望
2. **Pull Request**: コード改善や新機能
3. **ドキュメント**: 使用例やガイドの追加
4. **Input Provider**: サンプル実装の共有

### 開発ガイドライン

- [コントリビューションガイド](docs/CONTRIBUTING.md)
- [開発ワークフロー](.kiro/steering/development-workflow.md)
- [コードスタイル](docs/CODE_STYLE.md)

### コミュニティ

- **GitHub Issues**: バグ報告・機能要望
- **GitHub Discussions**: 質問・アイデア交換
- **Slack**: リアルタイム議論（招待制）

---

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

---

# English Version

**Okina is a quiet change detection tool for firmware and software updates.**

Okina is designed as a supplementary and insurance mechanism to reduce accidents caused by "not noticing" firmware updates for network equipment and infrastructure software.

🏮 Okina is like an old man sitting on the veranda watching the world. It quietly watches, notifies when things are different from before, and leaves judgment to humans.

## Why Okina?

### Realistic Accidents

The following accidents can realistically occur with firmware updates for network equipment and infrastructure software:

1. New firmware is released by the vendor
2. Technical staff did not notice this fact
3. Automatic or semi-automatic updates ran
4. Changes entered the environment without prior verification, causing problems

### The Essence of the Problem

The essence of this accident is not "someone is bad", but **the structure that assumes humans will "notice" has inherent risks**.

### Okina's Role

Okina is designed as a **supplementary and insurance mechanism** to reduce this "didn't notice".

## Design Philosophy (Important)

Understanding Okina's design philosophy is a prerequisite for proper use:

### Basic Principles

- Okina is **not the main character**
- Okina **does not judge**
- Okina **does not automatically apply**
- Okina **does not replace people or operations**

### Okina's Role

> **"Quietly notify when something is different"**

Not placing excessive trust or expectations on this tool is a prerequisite for use.

## Quick Start

### 1. Installation

```bash
# Install from PyPI (planned for future)
pip install okina

# Or install from source
git clone https://github.com/kamonabe/Okina.git
cd Okina
pip install -e .
```

### 2. Configuration

```bash
# Copy configuration sample
cp config/settings.yml.sample settings.yml

# Edit configuration (Slack Webhook URL, etc.)
vim settings.yml
```

### 3. Environment Variables

```bash
# Set Slack Webhook URL as environment variable
export OKINA_SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 4. Run Change Detection

```bash
# Validate configuration
okina config validate

# Run change detection
okina check

# Check status
okina status
```

## Commands

```bash
# Run change detection
okina check

# Show status
okina status

# Show history
okina history

# Validate configuration
okina config validate
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Okina（翁）- Quietly watching, gently notifying, leaving judgment to humans.**Quietly watches upstream changes and lets you know when something feels different.
