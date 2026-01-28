#!/usr/bin/env python3
"""
Slack設定の確認スクリプト

環境変数とWebhook URLの形式をチェックします。
"""

import os
import re


def check_slack_config():
    """Slack設定を確認"""
    print("=" * 60)
    print("Slack設定チェック")
    print("=" * 60)
    
    # 環境変数の確認
    webhook_url = os.getenv("OKINA_SLACK_WEBHOOK")
    
    if not webhook_url:
        print("\n❌ エラー: OKINA_SLACK_WEBHOOK環境変数が設定されていません")
        print("\n設定方法:")
        print('  export OKINA_SLACK_WEBHOOK="https://hooks.slack.com/services/..."')
        print("\nWebhook URLの取得方法:")
        print("1. Slackワークスペースの設定を開く")
        print("2. 「アプリを管理」→「Incoming Webhooks」を検索")
        print("3. 「Slackに追加」をクリック")
        print("4. 通知先チャンネルを選択")
        print("5. 表示されたWebhook URLをコピー")
        return False
    
    print(f"\n✅ 環境変数が設定されています")
    print(f"   値: {webhook_url[:50]}...")
    
    # Webhook URLの形式チェック
    slack_webhook_pattern = r'^https://hooks\.slack\.com/services/[A-Z0-9]+/[A-Z0-9]+/[a-zA-Z0-9]+$'
    
    if re.match(slack_webhook_pattern, webhook_url):
        print("\n✅ Webhook URLの形式が正しいです")
        return True
    else:
        print("\n❌ Webhook URLの形式が正しくありません")
        print("\n正しい形式:")
        print("  https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX")
        print("\n現在の値:")
        print(f"  {webhook_url}")
        print("\n対処方法:")
        print("1. Slackワークスペースで新しいWebhook URLを取得")
        print("2. 以下のコマンドで環境変数を設定:")
        print('   export OKINA_SLACK_WEBHOOK="https://hooks.slack.com/services/..."')
        return False


if __name__ == "__main__":
    success = check_slack_config()
    exit(0 if success else 1)
