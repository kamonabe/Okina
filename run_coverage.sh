#!/bin/bash
# Okina カバレッジ測定スクリプト

set -e

echo "🧪 Okinaのテストカバレッジを測定します..."

# テスト実行とカバレッジ測定
pytest tests/ \
    --cov=src/okina \
    --cov-report=html \
    --cov-report=term \
    --cov-report=xml \
    --cov-fail-under=80 \
    -v

echo ""
echo "📊 カバレッジレポートが生成されました:"
echo "   HTML: htmlcov/index.html"
echo "   XML:  coverage.xml"
echo ""
echo "🎯 目標カバレッジ: 90%以上"
echo "🚨 最低カバレッジ: 80%以上"