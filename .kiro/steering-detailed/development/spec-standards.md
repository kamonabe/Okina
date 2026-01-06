# 仕様書（Spec）標準ガイド

## 🎯 目的
全プロジェクト共通の仕様書作成標準を定義し、
一貫性があり品質の高い仕様書を実現する。

## 📋 Spec構造標準

### 必須ファイル構成
```
.kiro/specs/{feature-name}/
├── requirements.yml           # 要件定義（YAML構造化）
├── design.yml                # 設計書（YAML構造化）
├── tasks.yml                 # 実装タスク（YAML構造化）
└── README.md                 # 概要・ガイド（オプション）
```

### 命名規約
```bash
# ディレクトリ名：ケバブケース
notification-system/
change-monitor/
diff-analyzer/

# ファイル名：固定
requirements.yml  # 要件定義
design.yml       # 設計書
tasks.yml        # タスクリスト
```

## 📝 requirements.yml 標準

### 必須セクション
```yaml
metadata:
  title: "機能名"
  feature: "feature-name"
  status: "draft"  # draft | in-progress | completed | deprecated
  created: "YYYY-MM-DD"
  updated: "YYYY-MM-DD"
  version: "1.0.0"
  complexity: "medium"  # low | medium | high
  estimated-hours: 8

overview:
  description: |
    機能の概要（2-3文で簡潔に）
  background: |
    なぜ必要か、現状の問題点
  goals:
    - "目標1: 何を達成したいか"
    - "目標2: どのような状態を目指すか"

acceptance-criteria:
  - id: "AC-001"
    title: "受入基準のタイトル"
    priority: "high"  # high | medium | low
    type: "functional"  # functional | non-functional | security
    description: |
      詳細な説明
    when: "どのような条件・状況の時"
    then: "どのような結果が得られるべきか"
    examples:
      - input: "入力例"
        output: "期待される出力"

non-functional-requirements:
  performance:
    - "処理時間が100ms以内"
  reliability:
    - "エラー時も処理を継続"
  maintainability:
    - "設定ファイルで管理"

success-metrics:
  quantitative:
    - "テストカバレッジ95%以上"
  qualitative:
    - "ユーザーが便利と感じる"
```

### 品質基準
- **受入基準**: 最低3つ、各基準にWHEN-THEN形式
- **非機能要件**: 4カテゴリ（性能、信頼性、保守性、使いやすさ）
- **成功指標**: 定量的・定性的両方を含む
- **例**: 各受入基準に具体的な入出力例

## 🏗️ design.yml 標準

### 必須セクション
```yaml
metadata:
  title: "機能名"
  feature: "feature-name"
  status: "draft"
  created: "YYYY-MM-DD"
  updated: "YYYY-MM-DD"
  version: "1.0.0"

architecture:
  overview: |
    システム全体のアーキテクチャ概要
  components:
    - name: "コンポーネント名"
      type: "module"  # module | class | function
      responsibility: "責務"
      dependencies: ["依存先"]

modules:
  - name: "モジュール名"
    path: "src/{project}/{module}.py"
    description: |
      モジュールの詳細説明
    functions:
      - name: "関数名"
        parameters:
          - name: "パラメータ名"
            type: "型"
            description: "説明"
        returns:
          type: "戻り値の型"
          description: "戻り値の説明"

correctness-properties:
  - id: "P1"
    title: "プロパティのタイトル"
    type: "invariant"  # invariant | idempotence | monotonicity
    description: |
      プロパティの詳細説明
    validates: ["AC-001", "AC-002"]
    test-strategy: "property-based"
    implementation:
      framework: "hypothesis"
      strategy: "st.integers(min_value=1)"
      assertion: "検証する条件"

testing-strategy:
  property-tests:
    - property: "P1"
      file: "tests/test_{module}_properties.py"
  integration-tests:
    - validates: ["AC-001"]
      file: "tests/test_{module}_integration.py"
  unit-tests:
    - validates: ["AC-001"]
      file: "tests/test_{module}_unit.py"
```

### 品質基準
- **コンポーネント**: 最低2つ、責務と依存関係を明記
- **正確性プロパティ**: 最低3つ、hypothesis使用
- **テスト戦略**: 3種類（プロパティ、統合、ユニット）
- **モジュール設計**: 関数シグネチャを含む詳細設計

## 📋 tasks.yml 標準

### 必須セクション
```yaml
metadata:
  title: "機能名"
  feature: "feature-name"
  status: "pending"  # pending | in-progress | completed
  created: "YYYY-MM-DD"
  updated: "YYYY-MM-DD"
  version: "1.0.0"

tasks:
  - id: "T1"
    title: "タスクのタイトル"
    status: "pending"  # pending | in-progress | done
    priority: "high"  # high | medium | low
    estimated-hours: 2
    depends-on: []
    validates: ["AC-001", "AC-002"]
    description: |
      タスクの詳細説明
    subtasks:
      - "サブタスク1"
      - "サブタスク2"
    files:
      - path: "src/{project}/{module}.py"
        action: "create"  # create | update | delete
        lines: 200
    tests:
      - "tests/test_{module}.py"

completion-criteria:
  - id: "CC-001"
    description: "全テストがパス"
    status: "pending"
    validation: "pytest tests/ -v"
    result: null

execution-plan:
  critical-path:
    - "T1"
    - "T2"
  total-estimated-hours: 10
```

### 必須タスク種別
1. **実装タスク**: コア機能の実装
2. **プロパティテスト**: hypothesis使用
3. **統合テスト**: エンドツーエンド検証
4. **ユニットテスト**: 個別機能検証
5. **ドキュメント更新**: README、CHANGELOG
6. **手動検証**: 受入基準の確認

### 品質基準
- **トレーサビリティ**: 各タスクが受入基準（AC-XXX）を検証
- **依存関係**: depends-onで実行順序を明確化
- **完了基準**: 自動検証可能な基準を設定
- **工数見積**: 実装・テスト・ドキュメントを含む

## 🔧 テンプレート使用方法

### 1. 新機能Spec作成
```bash
# 機能ディレクトリ作成
mkdir -p .kiro/specs/{feature-name}

# テンプレートコピー
cp .kiro/templates/specs/requirements.yml.template .kiro/specs/{feature-name}/requirements.yml
cp .kiro/templates/specs/design.yml.template .kiro/specs/{feature-name}/design.yml
cp .kiro/templates/specs/tasks.yml.template .kiro/specs/{feature-name}/tasks.yml
```

### 2. プレースホルダー置換
```bash
# 一括置換（例）
sed -i 's/{機能名}/通知システム/g' .kiro/specs/notification-system/*.yml
sed -i 's/{feature-name}/notification-system/g' .kiro/specs/notification-system/*.yml
sed -i 's/YYYY-MM-DD/2025-01-06/g' .kiro/specs/notification-system/*.yml
```

### 3. 内容記入
- **requirements.yml**: 要件定義から開始
- **design.yml**: アーキテクチャ設計
- **tasks.yml**: 実装計画

## 🧪 品質検証

### 自動検証スクリプト
```bash
# Spec構造検証
python scripts/validate_specs.py

# 一貫性チェック
python scripts/check_spec_consistency.py

# トレーサビリティ検証
python scripts/check_traceability.py
```

### 検証項目
```yaml
structure_validation:
  - "必須ファイルの存在確認"
  - "YAML構文の正当性"
  - "必須フィールドの存在"
  - "データ型の整合性"

content_validation:
  - "受入基準の品質（WHEN-THEN形式）"
  - "プロパティテストの定義"
  - "タスクと要件のトレーサビリティ"
  - "工数見積の妥当性"

consistency_validation:
  - "requirements.yml ↔ design.yml の整合性"
  - "design.yml ↔ tasks.yml の整合性"
  - "受入基準とテスト戦略の対応"
  - "プロパティと検証タスクの対応"
```

## 📊 品質メトリクス

### 必須品質基準
```yaml
requirements_quality:
  acceptance_criteria: "≥ 3件"
  examples_per_criteria: "≥ 1件"
  non_functional_categories: "= 4カテゴリ"
  success_metrics: "定量的・定性的両方"

design_quality:
  components: "≥ 2件"
  correctness_properties: "≥ 3件"
  test_strategies: "= 3種類（プロパティ、統合、ユニット）"
  function_signatures: "全関数に定義"

tasks_quality:
  task_types: "≥ 6種類（実装、プロパティ、統合、ユニット、ドキュメント、検証）"
  traceability: "全タスクがAC-XXXを検証"
  completion_criteria: "≥ 5件"
  estimated_hours: "≥ 8時間"
```

## 🔄 Specライフサイクル

### ステータス管理
```yaml
status_flow:
  draft: "初期作成、レビュー前"
  in-progress: "レビュー中、修正中"
  completed: "承認済み、実装可能"
  deprecated: "廃止、アーカイブ"

validation_flow:
  created: "作成時の自動検証"
  updated: "更新時の差分検証"
  reviewed: "レビュー時の品質検証"
  approved: "承認時の最終検証"
```

### バージョニング
```yaml
versioning:
  major: "要件の大幅変更（1.0.0 → 2.0.0）"
  minor: "機能追加、設計変更（1.0.0 → 1.1.0）"
  patch: "軽微な修正、誤字訂正（1.0.0 → 1.0.1）"
```

## 🎯 プロジェクト固有カスタマイズ

### Komon固有
```yaml
komon_extensions:
  monitoring_properties:
    - "リアルタイム性"
    - "アラート精度"
    - "システム負荷"
  
  task_categories:
    - "監視ロジック実装"
    - "アラート生成"
    - "パフォーマンステスト"
```

### Okina固有
```yaml
okina_extensions:
  change_detection_properties:
    - "変化検知精度"
    - "差分抽出正確性"
    - "通知信頼性"
  
  task_categories:
    - "変化検知実装"
    - "差分抽出"
    - "通知システム"
    - "翁らしさ検証"
```

## 📋 Specチェックリスト

### 作成時
- [ ] テンプレートから作成
- [ ] 全プレースホルダーを置換
- [ ] 必須セクションを記入
- [ ] 自動検証をパス

### レビュー時
- [ ] 要件の妥当性確認
- [ ] 設計の技術的妥当性
- [ ] タスクの実装可能性
- [ ] 工数見積の妥当性

### 承認時
- [ ] 全品質基準を満たす
- [ ] ステークホルダー承認
- [ ] 実装準備完了
- [ ] CI/CD統合確認

## 🎯 適用プロジェクト

- ✅ Komon（既存テンプレートを標準化）
- ✅ Okina（新規適用）
- 🔄 今後の新プロジェクト全て

---

**最終更新**: 2025-01-06
**重要度**: 高（仕様品質標準化）