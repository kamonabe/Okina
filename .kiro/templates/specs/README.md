# 仕様書（Spec）テンプレート

このディレクトリには、全プロジェクト共通の仕様書作成テンプレートが含まれています。

## 📋 テンプレートファイル

- `requirements.yml.template`: 要件定義書のテンプレート
- `design.yml.template`: 設計書のテンプレート
- `tasks.yml.template`: 実装タスクのテンプレート

## 🚀 使い方

### 1. 新しい機能のSpecを作成

```bash
# 機能名のディレクトリを作成（ケバブケース）
mkdir -p .kiro/specs/{feature-name}

# テンプレートをコピー
cp .kiro/templates/specs/requirements.yml.template .kiro/specs/{feature-name}/requirements.yml
cp .kiro/templates/specs/design.yml.template .kiro/specs/{feature-name}/design.yml
cp .kiro/templates/specs/tasks.yml.template .kiro/specs/{feature-name}/tasks.yml
```

### 2. プレースホルダーを置換

各ファイルを開いて、以下のプレースホルダーを置換：

```bash
# 一括置換例
sed -i 's/{機能名}/通知システム/g' .kiro/specs/notification-system/*.yml
sed -i 's/{feature-name}/notification-system/g' .kiro/specs/notification-system/*.yml
sed -i 's/{project}/okina/g' .kiro/specs/notification-system/*.yml
sed -i 's/YYYY-MM-DD/2025-01-06/g' .kiro/specs/notification-system/*.yml
```

### 3. 内容を記入

#### requirements.yml
1. **overview**: 機能の概要、背景、目標を記入
2. **acceptance-criteria**: 最低3つの受入基準を定義
3. **non-functional-requirements**: 4カテゴリの非機能要件
4. **success-metrics**: 定量的・定性的指標

#### design.yml
1. **architecture**: システム全体の設計
2. **modules**: 詳細なモジュール設計
3. **correctness-properties**: 最低3つのプロパティ
4. **testing-strategy**: 3種類のテスト戦略

#### tasks.yml
1. **tasks**: 実装タスクを依存関係順に定義
2. **completion-criteria**: 完了基準を設定
3. **execution-plan**: 実行計画とクリティカルパス

## 🧪 品質検証

### 自動検証コマンド
```bash
# Spec構造検証
python scripts/validate_specs.py

# 一貫性チェック
python scripts/check_spec_consistency.py

# トレーサビリティ検証
python scripts/check_traceability.py
```

### 品質基準チェックリスト

#### requirements.yml
- [ ] 受入基準が最低3つ定義されている
- [ ] 各受入基準にWHEN-THEN形式の条件がある
- [ ] 各受入基準に具体的な例がある
- [ ] 非機能要件が4カテゴリ含まれている
- [ ] 成功指標に定量的・定性的両方がある

#### design.yml
- [ ] コンポーネントが最低2つ定義されている
- [ ] 正確性プロパティが最低3つ定義されている
- [ ] テスト戦略が3種類（プロパティ、統合、ユニット）含まれている
- [ ] 各モジュールに関数シグネチャがある
- [ ] データ構造が詳細に定義されている

#### tasks.yml
- [ ] 必須タスク種別が含まれている（実装、プロパティテスト、統合テスト、ユニットテスト、ドキュメント、検証）
- [ ] 各タスクが受入基準（AC-XXX）を検証している
- [ ] 依存関係が適切に設定されている
- [ ] 完了基準が最低5つ定義されている
- [ ] 工数見積が妥当である

## 📊 品質メトリクス

### 必須品質基準
```yaml
requirements_quality:
  acceptance_criteria: "≥ 3件"
  examples_per_criteria: "≥ 1件"
  non_functional_categories: "= 4カテゴリ"

design_quality:
  components: "≥ 2件"
  correctness_properties: "≥ 3件"
  test_strategies: "= 3種類"

tasks_quality:
  task_types: "≥ 6種類"
  traceability: "全タスクがAC-XXXを検証"
  completion_criteria: "≥ 5件"
```

## 🔄 Specライフサイクル

### ステータス管理
- **draft**: 初期作成、レビュー前
- **in-progress**: レビュー中、修正中
- **completed**: 承認済み、実装可能
- **deprecated**: 廃止、アーカイブ

### バージョニング
- **major**: 要件の大幅変更（1.0.0 → 2.0.0）
- **minor**: 機能追加、設計変更（1.0.0 → 1.1.0）
- **patch**: 軽微な修正、誤字訂正（1.0.0 → 1.0.1）

## 🎯 プロジェクト固有カスタマイズ

### Komon固有の拡張
```yaml
komon_extensions:
  monitoring_properties:
    - "リアルタイム性"
    - "アラート精度"
  task_categories:
    - "監視ロジック実装"
    - "パフォーマンステスト"
```

### Okina固有の拡張
```yaml
okina_extensions:
  change_detection_properties:
    - "変化検知精度"
    - "通知信頼性"
  task_categories:
    - "変化検知実装"
    - "翁らしさ検証"
```

## 📚 参考例

良いSpecの例として、以下を参照してください：

### Komonの例
- `Komon/.kiro/specs/notification-history/`
- `Komon/.kiro/specs/unified-notification-system/`

### 作成予定のOkinaの例
- `Okina/.kiro/specs/notification-system/`
- `Okina/.kiro/specs/change-monitor/`

## 🚨 よくある問題と対策

### 問題1: 受入基準が曖昧
**対策**: WHEN-THEN形式で具体的な条件と結果を記述

### 問題2: プロパティテストが不十分
**対策**: invariant、idempotence、monotonicityの3種類を含める

### 問題3: タスクと要件の対応が不明確
**対策**: 各タスクのvalidatesフィールドでAC-XXXを明記

### 問題4: 工数見積が不正確
**対策**: 実装、テスト、ドキュメントを含めた総合的な見積

## 🔧 自動化スクリプト

### validate_specs.py
- YAML構文チェック
- 必須フィールド検証
- 品質基準チェック

### check_spec_consistency.py
- requirements ↔ design の整合性
- design ↔ tasks の整合性
- トレーサビリティ検証

### check_traceability.py
- AC-XXX → プロパティ → タスクの対応
- 受入基準の網羅性確認

## 🎯 適用プロジェクト

- ✅ Komon（既存テンプレートを標準化）
- ✅ Okina（新規適用）
- 🔄 今後の新プロジェクト全て

---

**最終更新**: 2025-01-06
**テンプレートバージョン**: 1.0.0