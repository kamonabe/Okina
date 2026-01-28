#!/usr/bin/env python3
"""
Slack通知の実動作テストスクリプト

環境変数 OKINA_SLACK_WEBHOOK が設定されている必要があります。
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from okina.notification import NotificationManager


def test_slack_notification():
    """実際にSlack通知を送信してテスト"""
    print("=" * 60)
    print("Okina Slack通知テスト")
    print("=" * 60)
    
    # 環境変数の確認
    webhook_url = os.getenv("OKINA_SLACK_WEBHOOK")
    if not webhook_url:
        print("\n❌ エラー: OKINA_SLACK_WEBHOOK環境変数が設定されていません")
        print("\n設定方法:")
        print('  export OKINA_SLACK_WEBHOOK="https://hooks.slack.com/services/..."')
        return 1
    
    print(f"\n✅ Webhook URL: {webhook_url[:50]}...")
    
    # NotificationManagerの初期化
    print("\n【ステップ1】NotificationManagerの初期化")
    config = {
        "slack": {
            "enabled": True,
            "webhook_url": "env:OKINA_SLACK_WEBHOOK",
            "channel": "#alerts",
            "username": "Okina（翁）"
        }
    }
    
    try:
        manager = NotificationManager(config)
        print("✅ 初期化成功")
    except Exception as e:
        print(f"❌ 初期化失敗: {e}")
        return 1
    
    # テスト1: 変化検知通知
    print("\n【ステップ2】変化検知通知のテスト送信")
    changes = {
        "added": 2,
        "changed": 1,
        "removed": 0
    }
    
    try:
        result = manager.send_change_notification(
            source="test-source",
            changes=changes
        )
        
        if result:
            print("✅ 変化検知通知の送信に成功しました")
            print("\nSlackチャンネルを確認してください。")
            print("以下のようなメッセージが届いているはずです:")
            print("-" * 40)
            print("変化を検知しました")
            print("")
            print("ソース: test-source")
            print("新規追加: 2件")
            print("内容変更: 1件")
            print(f"時刻: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            print("-" * 40)
        else:
            print("❌ 変化検知通知の送信に失敗しました")
            return 1
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # テスト2: エラー通知
    print("\n【ステップ3】エラー通知のテスト送信")
    try:
        result = manager.send_error_notification(
            error_type="テストエラー",
            error_message="これはテスト用のエラー通知です",
            source="test-source"
        )
        
        if result:
            print("✅ エラー通知の送信に成功しました")
        else:
            print("⚠️  エラー通知の送信に失敗しました（継続性のため処理は続行）")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 完了
    print("\n" + "=" * 60)
    print("✅ Slack通知テストが完了しました")
    print("=" * 60)
    print("\nSlackチャンネルで以下を確認してください:")
    print("1. 変化検知通知が届いている")
    print("2. エラー通知が届いている")
    print("3. メッセージが翁らしく静かで簡潔")
    print("4. 絵文字が使われていない")
    
    return 0


if __name__ == "__main__":
    sys.exit(test_slack_notification())
