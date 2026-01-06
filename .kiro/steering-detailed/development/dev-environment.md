# 開発環境標準ガイド

## 🎯 目的
全プロジェクト共通の開発環境標準を定義し、
一貫した開発体験と品質を実現する。

## 🛠️ 標準開発環境

### Python環境
```yaml
python_environment:
  version: "3.10+"
  package_manager: "pip"
  virtual_environment: "venv"
  
  required_tools:
    - "black"      # コードフォーマッター
    - "flake8"     # リンター
    - "mypy"       # 型チェッカー
    - "pytest"     # テストフレームワーク
    - "hypothesis" # プロパティテスト
    - "coverage"   # カバレッジ測定
```

### エディタ設定（VS Code）
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### Git設定
```bash
# 必須Git設定
git config --global user.name "kamonabe"
git config --global user.email "kamonabe1927@gmail.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.autocrlf input
```

## 📋 標準設定ファイル

### pyproject.toml（推奨）
```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "PROJECT_NAME"
dynamic = ["version"]
description = "PROJECT_DESCRIPTION"
readme = "README.md"
license = {text = "MIT"}
authors = [{name = "kamonabe", email = "kamonabe1927@gmail.com"}]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
requires-python = ">=3.10"
dependencies = [
    "pyyaml>=6.0",
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=22.0.0",
    "flake8>=5.0.0",
    "mypy>=1.0.0",
    "hypothesis>=6.0.0",
]

[tool.setuptools_scm]
write_to = "src/PROJECT_NAME/_version.py"

[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
exclude = [
    ".git",
    "__pycache__",
    "build",
    "dist",
    ".venv",
    ".eggs",
    "*.egg-info",
]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "property: marks tests as property-based tests",
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/build/*",
    "*/dist/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
```

### pre-commit設定
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 22.12.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## 🚀 環境セットアップ自動化

### セットアップスクリプト
```bash
#!/bin/bash
# scripts/setup_dev_environment.sh

set -e

echo "🚀 開発環境をセットアップ中..."

# Python仮想環境作成
if [ ! -d "venv" ]; then
    echo "📦 Python仮想環境を作成中..."
    python3 -m venv venv
fi

# 仮想環境アクティベート
source venv/bin/activate

# 依存関係インストール
echo "📚 依存関係をインストール中..."
pip install --upgrade pip
pip install -e ".[dev]"

# pre-commitフック設定
echo "🔧 pre-commitフックを設定中..."
pre-commit install

# Git設定確認
echo "🔍 Git設定を確認中..."
if ! git config user.name | grep -q "kamonabe"; then
    echo "⚠️  Git設定を更新してください:"
    echo "  git config --global user.name 'kamonabe'"
    echo "  git config --global user.email 'kamonabe1927@gmail.com'"
fi

# 初期テスト実行
echo "🧪 初期テストを実行中..."
pytest tests/ -v

echo "✅ 開発環境のセットアップが完了しました！"
echo ""
echo "📋 次のステップ:"
echo "  1. source venv/bin/activate  # 仮想環境をアクティベート"
echo "  2. pytest tests/             # テスト実行"
echo "  3. black src/ tests/         # コードフォーマット"
echo "  4. flake8 src/ tests/        # リント実行"
```

### Makefile（開発タスク自動化）
```makefile
# Makefile
.PHONY: help install test lint format type-check clean dev-setup

help:  ## このヘルプメッセージを表示
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## 依存関係をインストール
	pip install -e ".[dev]"

test:  ## テストを実行
	pytest tests/ -v --cov=src --cov-report=html

test-fast:  ## 高速テストのみ実行
	pytest tests/ -v -m "not slow"

lint:  ## リント実行
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:  ## コードフォーマット
	black src/ tests/
	isort src/ tests/

type-check:  ## 型チェック
	mypy src/

quality:  ## 品質チェック一括実行
	make lint
	make type-check
	make test

clean:  ## 一時ファイル削除
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/

dev-setup:  ## 開発環境セットアップ
	./scripts/setup_dev_environment.sh

validate:  ## プロジェクト品質検証
	python scripts/validate_specs.py
	python scripts/check_spec_consistency.py
	make quality

release-check:  ## リリース前チェック
	make validate
	python scripts/check_version_consistency.py
	python scripts/generate_release_notes.py --dry-run
```

## 🔧 IDE統合

### VS Code拡張機能
```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.mypy-type-checker",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-toolsai.jupyter",
    "redhat.vscode-yaml",
    "yzhang.markdown-all-in-one",
    "streetsidesoftware.code-spell-checker"
  ]
}
```

### デバッグ設定
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      }
    },
    {
      "name": "Python: Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["tests/", "-v"],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

## 📊 環境品質チェック

### 環境検証スクリプト
```python
# scripts/validate_environment.py
import sys
import subprocess
import importlib.util

def check_python_version():
    """Python バージョンチェック"""
    if sys.version_info < (3, 10):
        return False, f"Python 3.10+ required, got {sys.version}"
    return True, f"Python {sys.version} ✓"

def check_required_tools():
    """必須ツールの存在チェック"""
    tools = ["black", "flake8", "mypy", "pytest"]
    results = []
    
    for tool in tools:
        spec = importlib.util.find_spec(tool)
        if spec is None:
            results.append((False, f"{tool} not installed"))
        else:
            results.append((True, f"{tool} ✓"))
    
    return results

def check_git_config():
    """Git設定チェック"""
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], 
            text=True
        ).strip()
        email = subprocess.check_output(
            ["git", "config", "user.email"], 
            text=True
        ).strip()
        
        if name == "kamonabe" and email == "kamonabe1927@gmail.com":
            return True, "Git config ✓"
        else:
            return False, f"Git config incorrect: {name} <{email}>"
    except subprocess.CalledProcessError:
        return False, "Git config not set"

def main():
    """環境検証メイン"""
    print("🔍 開発環境を検証中...")
    
    # Python バージョン
    ok, msg = check_python_version()
    print(f"  {msg}")
    if not ok:
        sys.exit(1)
    
    # 必須ツール
    for ok, msg in check_required_tools():
        print(f"  {msg}")
        if not ok:
            print(f"    → pip install {msg.split()[0]}")
    
    # Git設定
    ok, msg = check_git_config()
    print(f"  {msg}")
    if not ok:
        print("    → git config --global user.name 'kamonabe'")
        print("    → git config --global user.email 'kamonabe1927@gmail.com'")
    
    print("✅ 環境検証完了")

if __name__ == "__main__":
    main()
```

## 🎯 適用プロジェクト

- ✅ Komon（既存環境を標準化）
- ✅ Okina（新規適用）
- 🔄 今後の新プロジェクト全て

---

**最終更新**: 2025-01-06
**重要度**: 高（開発環境統一）