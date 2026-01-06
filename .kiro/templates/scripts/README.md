# 自動化スクリプトテンプレート

## 🎯 目的
全プロジェクト共通の自動化スクリプトテンプレートを提供し、
一貫した品質管理とメンテナンス作業を実現する。

## 📋 標準スクリプト一覧

### 品質管理スクリプト
- `validate_specs.py` - Spec構造・品質検証
- `check_spec_consistency.py` - Spec間の一貫性チェック
- `check_traceability.py` - 要件とタスクのトレーサビリティ検証
- `validate_code_quality.py` - コード品質総合チェック

### プロジェクト管理スクリプト
- `check_status_consistency.py` - ステータス整合性チェック
- `generate_release_notes.py` - リリースノート自動生成
- `check_version_consistency.py` - バージョン整合性チェック
- `update_project_metadata.py` - プロジェクトメタデータ更新

### 開発支援スクリプト
- `setup_dev_environment.py` - 開発環境セットアップ
- `run_all_tests.py` - 全テスト実行・レポート生成
- `check_dependencies.py` - 依存関係チェック・更新提案
- `generate_documentation.py` - ドキュメント自動生成

### セキュリティスクリプト
- `scan_secrets.py` - 機密情報スキャン
- `check_vulnerabilities.py` - 脆弱性チェック
- `validate_permissions.py` - ファイル権限チェック

## 🔧 使用方法

### 1. スクリプトテンプレートのコピー
```bash
# プロジェクトのscriptsディレクトリに必要なスクリプトをコピー
cp .kiro/templates/scripts/validate_specs.py PROJECT_NAME/scripts/
cp .kiro/templates/scripts/check_spec_consistency.py PROJECT_NAME/scripts/
```

### 2. プロジェクト固有の設定
各スクリプトの設定セクションを編集：
```python
# プロジェクト固有設定
PROJECT_NAME = "okina"  # または "komon"
SOURCE_DIR = "src"
SPEC_DIR = ".kiro/specs"
```

### 3. 実行
```bash
# 品質チェック一括実行
python scripts/validate_all.py

# 個別実行
python scripts/validate_specs.py
python scripts/check_spec_consistency.py
```

## 📊 品質メトリクス

### 自動収集される指標
- Spec品質スコア（0-100）
- コードカバレッジ率
- 依存関係の健全性
- セキュリティスコア
- ドキュメント完成度

### レポート出力
- HTML形式の詳細レポート
- JSON形式のメトリクスデータ
- CI/CD用の簡潔なサマリー

## 🎯 適用プロジェクト

- ✅ Komon（既存スクリプトを標準化）
- ✅ Okina（新規適用）
- 🔄 今後の新プロジェクト全て