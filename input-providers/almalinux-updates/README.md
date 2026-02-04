# AlmaLinux Updates Provider

AlmaLinux（RHEL系）システムで利用可能なパッケージ更新を自動検知し、Okinaプロジェクトの標準データ形式で出力するInput Provider。

## 概要

このプロバイダーは以下の機能を提供します：

- 現在インストールされているパッケージ情報の取得（rpm -qa）
- 利用可能な更新情報の取得（dnf check-update）
- セキュリティ更新の優先識別（CVE情報含む）
- パッケージ状態の統合分析（current, update_available, recently_updated）
- Okina標準形式（okina.item.v1）への変換

## 特徴

- **翁らしい静かな動作**: 不要な出力なし、推奨アクションなし
- **正確な差分検知**: 状態変化を適切に表現
- **タイムアウト制御**: dnfコマンドのハング対策（デフォルト5分）
- **エラー処理**: 静かにログ記録、次回実行で自然復旧

## 必要要件

- AlmaLinux 9（RHEL系Linux）
- Python 3.10+
- dnf, rpm コマンド

## インストール

```bash
cd input-providers/almalinux-updates
pip install -r requirements.txt
```

## 使用方法

```bash
# 基本実行
python -m almalinux_updates.main

# ドライラン
python -m almalinux_updates.main --dry-run
```

## 設定

`config.yml`で動作をカスタマイズできます。詳細は`config.yml.sample`を参照してください。

## 開発

```bash
# 開発依存関係のインストール
pip install -r requirements-dev.txt

# テスト実行
pytest tests/ -v

# カバレッジ確認
pytest --cov=src --cov-report=html

# コード品質チェック
black src/ tests/
flake8 src/ tests/
mypy src/
```

## ライセンス

MIT License

## 作者

kamonabe
