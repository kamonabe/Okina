#!/usr/bin/env python3
"""
通知システムの手動動作確認スクリプト

このスクリプトは実装された通知システムの動作を確認するために使用します。
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from okina.notification import NotificationManager, MessageFormatter


def test_message_formatter():
    """MessageFormatterの動作確認"""
    print("=" * 60)
    print("MessageFormatter 動作確認")
    print("=" * 60)
    
    formatter = MessageFormatter()
    
    # テストケース1: 変化検知メッセージ
    print("\n【テスト1】変化検知メッセージ")
    changes = {
        "added": 2,
        "changed": 1,
        "removed": 0
    }
    message = formatter.format_change_message(
        changes=changes,
        source="fortinet-docs"
    )
    print(message)
    
    # テストケース2: エラーメッセージ
    print("\n【テスト2】エラーメッセージ")
    error_message = formatter.format_error_message(
        error_type="接続エラー",
        error_message="API接続がタイムアウトしました",
        source="fortinet-docs"
    )
    print(error_message)
    
    # テストケース3: 変化なし
    print("\n【テスト3】変化なしの場合")
    no_changes = {
        "added": 0,
        "changed": 0,
        "removed": 0
    }
    message = formatter.format_change_message(
        changes=no_changes,
        source="fortinet-docs"
    )
    print(f"メッセージ: {message if message else '(通知なし - 翁らしく静かに見守る)'}")
    
    print("\n✅ MessageFormatter の動作確認完了")


def test_notification_manager():
    """NotificationManagerの動作確認（Slack通知なし）"""
    print("\n" + "=" * 60)
    print("NotificationManager 動作確認")
    print("=" * 60)
    
    # 設定なしで初期化
    print("\n【テスト1】設定なしで初期化")
    try:
        manager = NotificationManager()
        print("✅ 初期化成功（通知先なし）")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    # Slack設定ありで初期化（環境変数なし）
    print("\n【テスト2】Slack設定ありで初期化（環境変数なし）")
    config = {
        "slack": {
            "enabled": True,
            "webhook_url": "env:OKINA_SLACK_WEBHOOK_TEST"
        }
    }
    try:
        manager = NotificationManager(config)
        print("✅ 初期化成功（Slack設定あり、環境変数未設定）")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    print("\n✅ NotificationManager の動作確認完了")


def test_okina_behavior():
    """翁らしさの確認"""
    print("\n" + "=" * 60)
    print("翁らしさの確認")
    print("=" * 60)
    
    formatter = MessageFormatter()
    
    print("\n【確認1】絵文字を使わない")
    message = formatter.format_change_message(
        changes={"added": 1, "changed": 0, "removed": 0},
        source="test"
    )
    has_emoji = any(ord(c) > 127 for c in message if not c.isalpha())
    print(f"絵文字なし: {'✅' if not has_emoji else '❌'}")
    
    print("\n【確認2】判断的でない表現")
    # メッセージに判断的な単語が含まれていないか確認
    judgmental_words = ["すぐに", "急いで", "推奨", "必須", "重要", "緊急"]
    has_judgmental = any(word in message for word in judgmental_words)
    print(f"判断的でない: {'✅' if not has_judgmental else '❌'}")
    
    print("\n【確認3】簡潔で静か")
    line_count = len(message.split('\n'))
    print(f"行数: {line_count}行（簡潔: {'✅' if line_count <= 10 else '❌'}）")
    
    print("\n✅ 翁らしさの確認完了")


def main():
    """メイン処理"""
    print("\n" + "=" * 60)
    print("Okina 通知システム 手動動作確認")
    print("=" * 60)
    
    try:
        # 各テストを実行
        test_message_formatter()
        test_notification_manager()
        test_okina_behavior()
        
        print("\n" + "=" * 60)
        print("✅ 全ての動作確認が完了しました")
        print("=" * 60)
        
        print("\n【次のステップ】")
        print("1. 実際のSlack通知をテストする場合:")
        print("   export OKINA_SLACK_WEBHOOK='https://hooks.slack.com/services/...'")
        print("   python scripts/test_notification.py --with-slack")
        print("\n2. 本番環境での動作確認:")
        print("   okina check")
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
