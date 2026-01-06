# テスト戦略共通ルール

## 🎯 基本方針

全プロジェクトで**しっかりしたテスト**を維持し、品質を保証します。

## 🧪 テスト戦略

### テストカバレッジ目標
- **目標**: 95%以上
- **最低**: 90%以上
- **重要モジュール**: 95%以上

### テストレベル
1. **プロパティベーステスト**: hypothesis使用
2. **統合テスト**: 外部依存あり
3. **ユニットテスト**: 外部依存なし

### テスト実行
```bash
pytest tests/ -v
pytest --cov=src --cov-report=html
pytest tests/ -m "hypothesis"  # プロパティテストのみ
```

## 📊 3層テスト構造

### 1. プロパティベーステスト（Property-Based Testing）
**目的**: 仕様の正確性を数学的に検証する

**対象**:
- 不変条件（Invariants）
- 数学的な性質
- 境界値の挙動

**ファイル命名**: `test_{module}_properties.py`

**例**:
```python
from hypothesis import given, strategies as st

@given(st.lists(st.floats(min_value=0.0, max_value=100.0), min_size=2))
def test_property_calculation_accuracy(data):
    """
    任意のデータに対して、計算結果は数学的に正しい値でなければならない
    """
    result = calculate_average(data)
    expected = sum(data) / len(data)
    assert abs(result - expected) < 0.0001
```

**書くべきプロパティ**:
- ✅ 計算結果の正確性
- ✅ 不変条件
- ✅ 境界値の挙動
- ✅ 冪等性

**書かなくて良いもの**:
- ❌ ファイルI/O
- ❌ 外部API呼び出し
- ❌ 複数モジュールの連携

### 2. 統合テスト（Integration Testing）
**目的**: 複数モジュールの連携を検証する

**対象**:
- モジュール間のデータフロー
- ファイルI/O（実ファイル使用）
- エンドツーエンドの動作
- CLIコマンドの実行結果

**ファイル命名**: `test_{module}_integration.py`

**例**:
```python
def test_end_to_end_with_data(tmp_path, capsys):
    """
    エンドツーエンドの動作を確認
    """
    # 実際のファイルを作成（tmp_path使用）
    test_dir = tmp_path / "data"
    test_dir.mkdir()
    test_file = test_dir / "test.csv"
    test_file.write_text("timestamp,cpu,mem,disk\n2025-01-05 10:00:00,50.0,60.0,70.0")
    
    # モジュールを実行
    result = process_data(str(test_dir))
    
    # 結果を検証
    assert result['cpu'] == 50.0
```

### 3. ユニットテスト（Unit Testing）
**目的**: 個別関数のロジックを検証する

**対象**:
- 個別関数の動作
- エッジケースの処理
- エラーハンドリング

**ファイル命名**: `test_{module}_unit.py`

## 🔧 テスト設定

### pytest.ini
```ini
[pytest]
testpaths = tests
pythonpath = src
addopts = 
    -v
    --tb=short
    --strict-markers
    --junit-xml=test-results/junit.xml

markers =
    unit: ユニットテスト（外部依存なし）
    integration: 統合テスト（外部依存あり）
    hypothesis: プロパティベーステスト
    slow: 実行に時間がかかるテスト

python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### requirements-dev.txt
```
# テスト
pytest>=7.0.0
pytest-cov>=4.0.0
hypothesis>=6.0.0

# コード品質
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
```

## 📈 テスト品質指標

### カバレッジ測定
```bash
# カバレッジ測定
pytest --cov=src --cov-report=html --cov-report=term

# カバレッジ閾値チェック
pytest --cov=src --cov-fail-under=90
```

### テスト実行時間
- ユニットテスト: 1秒以内
- 統合テスト: 10秒以内
- プロパティテスト: 30秒以内

## 🎯 プロジェクト固有の調整

各プロジェクトは以下を調整可能：
- カバレッジ目標（90-95%の範囲）
- プロパティテストの重点領域
- 統合テストの範囲
- テスト実行時間の制限

## 🔄 継続的改善

### テスト品質の監視
- カバレッジの推移
- テスト実行時間の推移
- テスト失敗率の推移

### 定期的な見直し
- 月1回のテスト戦略レビュー
- 新機能追加時のテスト設計見直し
- パフォーマンス問題の特定と改善

## 🎯 適用プロジェクト

- ✅ Komon
- ✅ Okina
- 🔄 今後の新プロジェクト全て