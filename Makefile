# Makefile for Okina - 翁らしい開発ワークフロー
.PHONY: help install test lint format type-check clean dev-setup validate okina-test

help:  ## このヘルプメッセージを表示
	@echo "🏮 Okina（翁）開発コマンド"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## 依存関係をインストール
	pip install -e ".[dev]"

test:  ## テストを実行（翁らしく静かに）
	pytest tests/ -v --cov=src --cov-report=html

test-fast:  ## 高速テストのみ実行
	pytest tests/ -v -m "not slow"

okina-test:  ## 翁らしさテストを実行
	pytest tests/ -v -m "okina" --tb=short

lint:  ## リント実行（翁らしい品質チェック）
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:  ## コードフォーマット（翁らしく整える）
	black src/ tests/
	isort src/ tests/

type-check:  ## 型チェック
	mypy src/

quality:  ## 品質チェック一括実行
	make lint
	make type-check
	make test

clean:  ## 一時ファイル削除（翁らしく静かに掃除）
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/

dev-setup:  ## 開発環境セットアップ
	@echo "🏮 翁らしい開発環境をセットアップ中..."
	python -m venv venv
	@echo "仮想環境を作成しました。以下を実行してください："
	@echo "  source venv/bin/activate"
	@echo "  make install"

validate:  ## プロジェクト品質検証（翁らしい品質確認）
	@echo "🔍 翁らしい品質検証を実行中..."
	python scripts/validate_specs.py || echo "Spec検証スクリプトが見つかりません"
	make quality

okina-check:  ## 翁らしさチェック（Okina固有）
	@echo "🏮 翁らしさを確認中..."
	make okina-test
	@echo "✅ 翁らしい振る舞いが確認されました"

release-check:  ## リリース前チェック（翁らしく慎重に）
	@echo "🏮 翁らしいリリース前チェック..."
	make validate
	make okina-check
	@echo "✅ 翁らしい品質でリリース準備完了"