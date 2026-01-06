# CI/CD標準ガイド

## 🎯 目的
全プロジェクト共通のCI/CD標準を定義し、
自動化された品質管理とデプロイメントを実現する。

## 🚀 GitHub Actions標準設定

### 基本ワークフロー構成
```
.github/workflows/
├── tests.yml                  # テスト・品質チェック
├── release.yml                # リリース自動化
├── security.yml               # セキュリティチェック
└── docs.yml                   # ドキュメント生成
```

## 🧪 tests.yml - テスト・品質チェック

### 標準テンプレート
```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    - name: Code formatting check
      run: |
        black --check src/ tests/ scripts/
        isort --check-only src/ tests/ scripts/
    
    - name: Lint check
      run: |
        flake8 src/ tests/ scripts/
    
    - name: Type check
      run: |
        mypy src/
    
    - name: Security check
      run: |
        bandit -r src/
        safety check
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
    
    - name: Spec validation
      run: |
        python scripts/validate_specs.py
    
    - name: Check status consistency
      run: |
        python scripts/check_status_consistency.py

  property-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    - name: Run property tests
      run: |
        pytest tests/property/ -v --hypothesis-show-statistics
```

## 🚀 release.yml - リリース自動化

### リリースワークフロー
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
        pip install -r requirements-dev.txt
    
    - name: Run full test suite
      run: |
        pytest tests/ --cov=src --cov-report=xml
        python scripts/validate_specs.py
    
    - name: Build package
      run: |
        python -m build
    
    - name: Check package
      run: |
        twine check dist/*
    
    - name: Generate release notes
      run: |
        python scripts/generate_release_notes.py > release_notes.md
    
    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body_path: release_notes.md
        draft: false
        prerelease: false
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        twine upload dist/*
```

## 🛡️ security.yml - セキュリティチェック

### セキュリティワークフロー
```yaml
name: Security

on:
  schedule:
    - cron: '0 2 * * 1'  # 毎週月曜日 2:00 UTC
  push:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install safety bandit pip-audit
        pip install -r requirements.txt
    
    - name: Run safety check
      run: |
        safety check --json --output safety-report.json
    
    - name: Run bandit security linter
      run: |
        bandit -r src/ -f json -o bandit-report.json
    
    - name: Run pip-audit
      run: |
        pip-audit --format=json --output=pip-audit-report.json
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          safety-report.json
          bandit-report.json
          pip-audit-report.json

  secrets-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Run TruffleHog OSS
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: main
        head: HEAD
```

## 📚 docs.yml - ドキュメント生成

### ドキュメントワークフロー
```yaml
name: Documentation

on:
  push:
    branches: [ main ]
    paths: [ 'docs/**', 'src/**/*.py' ]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install sphinx sphinx-rtd-theme
        pip install -r requirements.txt
    
    - name: Generate API documentation
      run: |
        sphinx-apidoc -o docs/api src/
    
    - name: Build documentation
      run: |
        cd docs
        make html
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/_build/html
```

## 🔧 品質ゲート設定

### 必須チェック項目
```yaml
# .github/branch_protection.yml
protection_rules:
  main:
    required_status_checks:
      strict: true
      contexts:
        - "test (3.10)"
        - "test (3.11)" 
        - "test (3.12)"
        - "property-tests"
        - "security"
    enforce_admins: true
    required_pull_request_reviews:
      required_approving_review_count: 1
      dismiss_stale_reviews: true
    restrictions: null
```

### 品質基準
```yaml
# 必須品質基準
quality_gates:
  test_coverage: 90%          # テストカバレッジ
  code_quality: A             # コード品質グレード
  security_issues: 0          # セキュリティ問題
  lint_errors: 0              # リントエラー
  type_errors: 0              # 型エラー
```

## 🚨 エラーハンドリング

### 失敗時の対応
```yaml
# テスト失敗時の通知
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    channel: '#ci-alerts'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### リトライ設定
```yaml
# 不安定なテストのリトライ
- name: Run flaky tests
  uses: nick-invision/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: pytest tests/integration/ -v
```

## 📊 メトリクス収集

### パフォーマンス測定
```yaml
- name: Performance benchmarks
  run: |
    pytest tests/benchmarks/ --benchmark-json=benchmark.json

- name: Upload benchmark results
  uses: benchmark-action/github-action-benchmark@v1
  with:
    tool: 'pytest'
    output-file-path: benchmark.json
    github-token: ${{ secrets.GITHUB_TOKEN }}
    auto-push: true
```

### カバレッジ追跡
```yaml
- name: Coverage comment
  uses: py-cov-action/python-coverage-comment-action@v3
  with:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    MINIMUM_GREEN: 90
    MINIMUM_ORANGE: 80
```

## 🔐 シークレット管理

### 必要なシークレット
```bash
# GitHub Secrets設定
PYPI_API_TOKEN          # PyPI公開用
CODECOV_TOKEN           # カバレッジ報告用
SLACK_WEBHOOK           # 通知用
SONAR_TOKEN             # コード品質分析用
```

### 環境変数設定
```yaml
env:
  PYTHONPATH: ${{ github.workspace }}/src
  COVERAGE_FILE: .coverage
  HYPOTHESIS_PROFILE: ci
```

## 📋 CI/CD設定チェックリスト

### 初期設定
- [ ] GitHub Actionsワークフロー作成
- [ ] 必要なシークレット設定
- [ ] ブランチ保護ルール設定
- [ ] 品質ゲート設定

### 定期メンテナンス
- [ ] 依存関係の更新（月1回）
- [ ] セキュリティチェック結果確認
- [ ] パフォーマンス指標確認
- [ ] ワークフロー実行時間最適化

### リリース前
- [ ] 全テスト成功確認
- [ ] カバレッジ基準達成確認
- [ ] セキュリティ問題なし確認
- [ ] ドキュメント更新確認

## 🎯 プロジェクト固有設定

### Komon固有
```yaml
# Komon特有のテスト
- name: Spec consistency check
  run: python scripts/check_spec_consistency.py

- name: Task status validation
  run: python scripts/validate_task_status.py
```

### Okina固有
```yaml
# Okina特有のテスト
- name: Notification system test
  run: pytest tests/integration/test_notification_flow.py

- name: Change detection accuracy test
  run: pytest tests/property/test_change_detection.py
```

## 🎯 適用プロジェクト

- ✅ Komon
- ✅ Okina
- 🔄 今後の新プロジェクト全て

---

**最終更新**: 2025-01-06
**重要度**: 高（自動化・品質保証）