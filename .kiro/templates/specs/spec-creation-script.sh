#!/bin/bash

# 仕様書作成スクリプト
# 使用方法: ./spec-creation-script.sh <feature-name> <project-name> <機能名>
# 例: ./spec-creation-script.sh notification-system okina "通知システム"

set -e

# 引数チェック
if [ $# -ne 3 ]; then
    echo "使用方法: $0 <feature-name> <project-name> <機能名>"
    echo "例: $0 notification-system okina \"通知システム\""
    exit 1
fi

FEATURE_NAME="$1"
PROJECT_NAME="$2"
FEATURE_TITLE="$3"
CURRENT_DATE=$(date +%Y-%m-%d)

# プロジェクトルートディレクトリを検出
if [ -d "$PROJECT_NAME" ]; then
    PROJECT_ROOT="$PROJECT_NAME"
elif [ -f "setup.py" ] && grep -q "$PROJECT_NAME" setup.py; then
    PROJECT_ROOT="."
else
    echo "エラー: プロジェクト '$PROJECT_NAME' が見つかりません"
    exit 1
fi

SPEC_DIR="$PROJECT_ROOT/.kiro/specs/$FEATURE_NAME"
TEMPLATE_DIR=".kiro/templates/specs"

echo "🚀 仕様書を作成中..."
echo "  機能名: $FEATURE_TITLE"
echo "  feature-name: $FEATURE_NAME"
echo "  プロジェクト: $PROJECT_NAME"
echo "  作成日: $CURRENT_DATE"
echo "  出力先: $SPEC_DIR"

# ディレクトリ作成
mkdir -p "$SPEC_DIR"

# テンプレートの存在確認
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "エラー: テンプレートディレクトリが見つかりません: $TEMPLATE_DIR"
    exit 1
fi

# テンプレートファイルをコピーして置換
for template in requirements.yml.template design.yml.template tasks.yml.template; do
    if [ ! -f "$TEMPLATE_DIR/$template" ]; then
        echo "エラー: テンプレートファイルが見つかりません: $TEMPLATE_DIR/$template"
        exit 1
    fi
    
    output_file="$SPEC_DIR/${template%.template}"
    
    echo "  📝 $output_file を作成中..."
    
    # プレースホルダーを置換
    sed -e "s/{機能名}/$FEATURE_TITLE/g" \
        -e "s/{feature-name}/$FEATURE_NAME/g" \
        -e "s/{project}/$PROJECT_NAME/g" \
        -e "s/YYYY-MM-DD/$CURRENT_DATE/g" \
        "$TEMPLATE_DIR/$template" > "$output_file"
done

echo ""
echo "✅ 仕様書の作成が完了しました！"
echo ""
echo "📋 次のステップ:"
echo "  1. $SPEC_DIR/requirements.yml を編集して要件を定義"
echo "  2. $SPEC_DIR/design.yml を編集して設計を記述"
echo "  3. $SPEC_DIR/tasks.yml を編集して実装計画を作成"
echo ""
echo "🧪 品質検証:"
echo "  python scripts/validate_specs.py"
echo "  python scripts/check_spec_consistency.py"
echo ""
echo "📚 参考:"
echo "  .kiro/templates/specs/README.md - テンプレート使用ガイド"
echo "  .kiro/steering-detailed/development/spec-standards.md - 仕様書標準"

# 作成されたファイルの一覧表示
echo ""
echo "📁 作成されたファイル:"
ls -la "$SPEC_DIR"