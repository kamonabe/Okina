# Okina 使用例・出力例

このドキュメントでは、Okinaの実際の使用例と出力例を示します。

---

## 📋 目次

- [基本的な使用例](#基本的な使用例)
- [通知メッセージ例](#通知メッセージ例)
- [設定ファイル例](#設定ファイル例)
- [cron設定例](#cron設定例)
- [Input Provider例](#input-provider例)

---

## 基本的な使用例

### 変化検知の実行

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

### ステータス確認

```bash
$ okina status

📊 Okina ステータス

最終実行: 2025-12-22 14:30:00
ステータス: 正常
検知件数: 3件（新規2件、変更1件）

データソース:
  • fortinet-docs: 最終更新 2025-12-22 14:30:00
  • cisco-docs: 最終更新 2025-12-22 09:00:00

通知設定:
  • Slack: 有効
  • 運用チーム: #ops-alerts
  • 開発チーム: #dev-alerts
```

### 履歴表示

```bash
$ okina history --limit 5

📜 変化検知履歴（最新5件）

2025-12-22 14:30:00 | fortinet-docs
  新規: 2件, 変更: 1件, 削除: 0件

2025-12-21 09:00:00 | fortinet-docs
  新規: 0件, 変更: 1件, 削除: 0件

2025-12-20 09:00:00 | cisco-docs
  新規: 1件, 変更: 0件, 削除: 0件

2025-12-19 09:00:00 | fortinet-docs
  変化なし

2025-12-18 09:00:00 | fortinet-docs
  新規: 3件, 変更: 0件, 削除: 1件
```

---

## 通知メッセージ例

### 変化検知通知（運用チーム向け）

翁らしい静かで簡潔なメッセージ形式：

```
変化を検知しました

ソース: fortinet-docs
新規追加: 2件
内容変更: 1件
削除: 0件
時刻: 2026-01-07 09:00
```

**特徴**:
- 絵文字なし
- 事実のみを記載
- 判断的な表現を避ける
- 必要な情報のみを含む

### エラー通知（開発チーム向け）

```
エラーを検知しました

種類: 接続エラー
詳細: API接続がタイムアウトしました
ソース: fortinet-docs
時刻: 2026-01-07 14:00
```

### 変化なしの場合

変化がない場合は**通知を送信しません**（翁らしく静かに見守る）。

---

## 設定ファイル例

### config/notification.yml

```yaml
# Okina 通知設定

# 運用チーム向け変化通知
change_reports:
  slack:
    enabled: true
    webhook_url: "env:OKINA_SLACK_WEBHOOK_OPS"
    channel: "#ops-alerts"
  schedule: "daily"  # daily | hourly
  time: "09:00"
  weekends: false  # 土日は通知しない

# 開発チーム向けエラー通知
error_alerts:
  slack:
    enabled: true
    webhook_url: "env:OKINA_SLACK_WEBHOOK_DEV"
    channel: "#dev-alerts"
  schedule: "hourly"
  business_hours_only: true  # 営業時間内のみ（9-18時）
```

### settings.yml（メイン設定）

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
  config_file: "config/notification.yml"

output:
  default_mode: "normal"  # normal | verbose | quiet
  max_items_per_notification: 10
```

---

## cron設定例

### 運用チーム向け（毎日朝9時）

```bash
# /etc/cron.d/okina-daily
0 9 * * * okina /usr/local/bin/okina check >> /var/log/okina/daily.log 2>&1
```

### 開発チーム向け（営業時間内毎時）

```bash
# /etc/cron.d/okina-hourly
0 9-18 * * 1-5 okina /usr/local/bin/okina check --error-only >> /var/log/okina/hourly.log 2>&1
```

### systemd-timer設定

```ini
# /etc/systemd/system/okina-daily.service
[Unit]
Description=Okina Daily Change Detection
After=network.target

[Service]
Type=oneshot
User=okina
WorkingDirectory=/opt/okina
ExecStart=/usr/local/bin/okina check
Environment=OKINA_SLACK_WEBHOOK_OPS=https://hooks.slack.com/services/...
Environment=OKINA_SLACK_WEBHOOK_DEV=https://hooks.slack.com/services/...

# /etc/systemd/system/okina-daily.timer
[Unit]
Description=Run Okina daily at 9:00
Requires=okina-daily.service

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

有効化：

```bash
sudo systemctl enable okina-daily.timer
sudo systemctl start okina-daily.timer
sudo systemctl status okina-daily.timer
```

---

## Input Provider例

### Fortinet ドキュメント用 Input Provider

```python
#!/usr/bin/env python3
"""
Fortinet ドキュメント用 Input Provider
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
            "version": "7.6.7",
            "title": "FortiOS 7.6.7 Release Notes",
            "url": "https://docs.fortinet.com/document/fortigate/7.6.7/fortios-release-notes",
            "pdf_url": "https://docs.fortinet.com/document/fortigate/7.6.7/fortios-release-notes/pdf"
        },
        {
            "version": "7.4.5",
            "title": "FortiAnalyzer 7.4.5 Release Notes",
            "url": "https://docs.fortinet.com/document/fortianalyzer/7.4.5/release-notes",
            "pdf_url": "https://docs.fortinet.com/document/fortianalyzer/7.4.5/release-notes/pdf"
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

### 正規化データ出力例（fortinet.jsonl）

```jsonl
{"schema": "okina.item.v1", "source": "fortinet-docs", "id": "fortinet:fortios:7.6.7:release", "type": "release", "title": "FortiOS 7.6.7 Release Notes", "version": "7.6.7", "url": "https://docs.fortinet.com/document/fortigate/7.6.7/fortios-release-notes", "observed_at": "2026-01-07T14:30:00+09:00", "payload": {"major": "7.6", "pdf_url": "https://docs.fortinet.com/document/fortigate/7.6.7/fortios-release-notes/pdf"}}
{"schema": "okina.item.v1", "source": "fortinet-docs", "id": "fortinet:fortianalyzer:7.4.5:release", "type": "release", "title": "FortiAnalyzer 7.4.5 Release Notes", "version": "7.4.5", "url": "https://docs.fortinet.com/document/fortianalyzer/7.4.5/release-notes", "observed_at": "2026-01-07T14:30:00+09:00", "payload": {"major": "7.4", "pdf_url": "https://docs.fortinet.com/document/fortianalyzer/7.4.5/release-notes/pdf"}}
```

---

## エラーハンドリング例

### 通知送信失敗時

```bash
$ okina check

🔍 変化検知を実行中...

📊 検知結果
ソース: fortinet-docs
新規追加: 2件

⚠️  Slack通知の送信に失敗しました
詳細: Connection timeout
処理は継続します（翁らしい継続性）
```

### 設定ファイル読み込み失敗時

```bash
$ okina check

❌ エラー: 設定ファイルの読み込みに失敗しました

ファイル: config/notification.yml
原因: ファイルが見つかりません

対処方法:
1. config/settings.yml.sample をコピーして設定ファイルを作成
2. 必要な設定項目を記入
3. 再度実行してください
```

---

## 翁らしさの実例

### ❌ 翁らしくない例

```
🚨 緊急！新しいファームウェアが公開されました！
すぐに確認して対応してください！！！

📢 重要なお知らせ
FortiOS 7.6.7がリリースされました。
早急にアップデートを検討することを強く推奨します。
```

### ✅ 翁らしい例

```
変化を検知しました

ソース: fortinet-docs
新規追加: 1件
時刻: 2026-01-07 09:00
```

**違い**:
- 絵文字を使わない
- 判断や推奨を含めない
- 事実のみを静かに伝える
- 人間の判断を尊重する

---

## よくある質問と出力例

### Q: 変化がない場合はどうなりますか？

A: 通知は送信されません。翁は静かに見守ります。

```bash
$ okina check

🔍 変化検知を実行中...

変化はありませんでした
（通知は送信されません）
```

### Q: 複数のソースを監視している場合は？

A: ソースごとに個別に通知されます。

```
変化を検知しました

ソース: fortinet-docs
新規追加: 2件
時刻: 2026-01-07 09:00

---

変化を検知しました

ソース: cisco-docs
内容変更: 1件
時刻: 2026-01-07 09:00
```

---

**Okina（翁）- 静かに見守り、変化があれば知らせ、判断は人に委ねます。**
