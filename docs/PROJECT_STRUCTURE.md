# Okinaプロジェクト構造

このドキュメントでは、Okinaプロジェクトのディレクトリ構造とファイル配置について説明します。

## ディレクトリ構造

```
Okina/
├── src/okina/              # コアモジュール（Pythonパッケージ）
├── scripts/                # 実行スクリプト
├── config/                 # 設定ファイルのサンプル
├── docs/                   # ドキュメント
├── tests/                  # テストコード
├── data/                   # 実行時データ（自動生成）
├── log/                    # ログファイル（自動生成）
└── .kiro/                  # Kiro IDE設定
```

## 各ディレクトリの詳細

### src/okina/

Okinaのコアロジックを含むPythonパッケージです。

- `__init__.py`: パッケージ初期化
- `monitor.py`: 変化監視機能
- `analyzer.py`: 差分分析・検出
- `notification.py`: 通知機能（Slack/メール）
- `cli.py`: CLIエントリーポイント
- `settings_validator.py`: 設定ファイル検証

### scripts/

実行可能なスクリプトファイルです。

- `check.py`: 変化検知のメインスクリプト
- `status.py`: ステータス表示
- `history.py`: 履歴表示
- `config_validate.py`: 設定検証

### config/

設定ファイルのサンプルを格納します。

- `settings.yml.sample`: 設定ファイルのサンプル

実際の`settings.yml`はプロジェクトルートに配置します。

### docs/

プロジェクトのドキュメントを格納します。

- `README.md`: 詳細なドキュメント
- `CHANGELOG.md`: 変更履歴
- `PROJECT_STRUCTURE.md`: このファイル
- `COMMAND_REFERENCE.md`: コマンドリファレンス

### tests/

テストコードを格納します。

```
tests/
├── conftest.py                    # pytest設定
├── test_monitor.py                # 変化監視テスト
├── test_analyzer.py               # 差分分析テスト
├── test_notification.py           # 通知機能テスト
├── test_cli.py                    # CLIテスト
└── README.md                      # テストドキュメント
```

### data/

実行時に自動生成されるデータディレクトリです。

```
data/
├── input/                  # Input Providerからの正規化データ
│   ├── fortinet.jsonl
│   └── cisco.jsonl
├── history/                # 前回データの保存
│   ├── fortinet_20251222.json
│   └── cisco_20251222.json
└── notifications/          # 通知履歴
    └── queue.json
```

### log/

ログファイルを格納します（自動生成）。

```
log/
├── okina.log               # メインログ
├── okina_error.log         # エラーログ
└── cron_check.log          # cron実行ログ
```

### .kiro/

Kiro IDE用の設定とspecファイルを格納します。

```
.kiro/
├── specs/                      # 仕様書
│   └── okina-system.md         # システム仕様書
├── tasks/                      # タスク管理
│   └── implementation-tasks.md # 実装タスクリスト
└── steering/                   # ステアリングルール
    └── development-workflow.md # 開発ワークフロー
```

## ファイル配置の原則

### 1. コアロジックとスクリプトの分離

- `src/okina/`: 再利用可能なビジネスロジック
- `scripts/`: 実行エントリーポイント

### 2. 設定とデータの分離

- `config/`: 設定テンプレート
- `data/`: 実行時データ（.gitignoreで除外）

### 3. ドキュメントの体系化

- `docs/`: ユーザー向けドキュメント
- `.kiro/specs/`: 開発者向け仕様書

### 4. テストの独立性

- `tests/`: 本体コードと分離
- カバレッジ90%以上を目標

## データフロー

```
Input Provider → data/input/*.jsonl → Okina → data/history/ → 通知
```

1. Input Providerが`data/input/`に正規化データを配置
2. Okinaが前回データ（`data/history/`）と比較
3. 差分があれば通知
4. 今回データを`data/history/`に保存