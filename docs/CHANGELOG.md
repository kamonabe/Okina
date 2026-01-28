# Changelog

All notable changes to Okina will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 通知システムの初期実装
  - `NotificationManager`: 通知の統合管理クラス
  - `MessageFormatter`: 翁らしいメッセージフォーマット生成
  - `SlackNotifier`: Slack API経由での通知送信
- 翁らしい静かで簡潔なメッセージ形式
  - 絵文字なし、事実ベースの内容
  - 判断的でない表現
- 環境変数による機密情報管理（`env:` プレフィックス）
- エラー時継続性の実装（翁らしく静かに処理を続ける）
- 包括的なテストスイート（カバレッジ93%）
  - 翁らしさを検証する21件のテスト
  - ユニットテスト、統合テスト

### Changed
- なし

### Deprecated
- なし

### Removed
- なし

### Fixed
- なし

### Security
- Webhook URLを環境変数で管理し、設定ファイルに直接記載しない仕組み

## [0.1.0] - 未リリース

### 初回リリース準備中
- プロジェクト基盤の確立
- 通知システムのコア機能実装
- ドキュメント整備

---

## リリースノート形式

各リリースには以下の情報を含めます：

- **Added**: 新機能
- **Changed**: 既存機能の変更
- **Deprecated**: 非推奨となった機能
- **Removed**: 削除された機能
- **Fixed**: バグ修正
- **Security**: セキュリティ関連の変更
