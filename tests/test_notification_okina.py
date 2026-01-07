#!/usr/bin/env python3
"""
通知システムの翁らしさテスト

このテストモジュールは通知システムが翁らしい振る舞いを
維持していることを検証します。

Author: kamonabe
Created: 2026-01-06
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from okina.notification import MessageFormatter, NotificationManager, SlackNotifier


class TestOkinaBehavior:
    """翁らしい振る舞いのテスト"""

    def test_never_suggests_automatic_action(self):
        """自動アクションを提案しないことを確認"""
        formatter = MessageFormatter()
        changes = {"added": 2, "changed": 1, "removed": 0}
        message = formatter.format_change_message(changes, "test-source")

        # 自動アクションを示唆する言葉が含まれていないことを確認
        forbidden_words = ["自動的に", "自動更新", "自動適用", "自動実行"]
        for word in forbidden_words:
            assert word not in message, f"Message should not contain '{word}'"

    def test_always_defers_to_human_judgment(self):
        """常に人間の判断に委ねることを確認"""
        formatter = MessageFormatter()
        changes = {"added": 2, "changed": 1, "removed": 0}
        message = formatter.format_change_message(changes, "test-source")

        # 人間の確認を促す表現が含まれていることを確認
        assert "確認" in message or "詳細" in message

        # 判断的な表現が含まれていないことを確認
        judgmental_words = ["すべき", "必要", "推奨", "おすすめ"]
        for word in judgmental_words:
            assert (
                word not in message
            ), f"Message should not contain judgmental word '{word}'"

    def test_quiet_and_humble_tone(self):
        """静かで控えめなトーンを確認"""
        formatter = MessageFormatter()
        changes = {"added": 2, "changed": 1, "removed": 0}
        message = formatter.format_change_message(changes, "test-source")

        # 翁らしい表現が含まれていることを確認
        assert "🏮 Okina（翁）" in message
        assert "詳細は okina history で確認できます" in message

        # 過度に主張的でないことを確認
        assertive_words = ["重要", "緊急", "至急", "必須"]
        for word in assertive_words:
            assert word not in message, f"Message should not be assertive with '{word}'"

    def test_no_changes_means_silence(self):
        """変化がない場合は静かに見守ることを確認"""
        formatter = MessageFormatter()

        # 変化がない場合
        no_changes = {"added": 0, "changed": 0, "removed": 0}
        message = formatter.format_change_message(no_changes, "test-source")

        # 空のメッセージ（静かに見守る）
        assert message == ""

        # 空の辞書の場合も同様
        empty_changes = {}
        message = formatter.format_change_message(empty_changes, "test-source")
        assert message == ""

    def test_error_handling_shows_continuity(self):
        """エラー時も継続性を示すことを確認"""
        formatter = MessageFormatter()
        error_message = formatter.format_error_message(
            "connection", "Network timeout", "test-source"
        )

        # 継続性を示す表現が含まれていることを確認
        assert "監視は継続" in error_message or "見守り続け" in error_message

        # パニックを起こさない表現であることを確認
        panic_words = ["危険", "緊急事態", "システム停止", "致命的"]
        for word in panic_words:
            assert (
                word not in error_message
            ), f"Error message should not cause panic with '{word}'"


class TestMessageFormatter:
    """MessageFormatterクラスのテスト"""

    def test_format_change_message_basic(self):
        """基本的な変化メッセージのフォーマットテスト"""
        formatter = MessageFormatter()
        changes = {"added": 2, "changed": 1, "removed": 0}
        timestamp = datetime(2026, 1, 6, 14, 30, 0)

        message = formatter.format_change_message(changes, "fortinet-docs", timestamp)

        # 必要な要素が含まれていることを確認
        assert "🏮 Okina（翁）からのお知らせ" in message
        assert "2026-01-06 14:30:00" in message
        assert "🔍 ソース: fortinet-docs" in message
        assert "✨ 新規追加: 2件" in message
        assert "🔄 内容変更: 1件" in message
        assert "詳細は okina history で確認できます" in message

        # 削除がない場合は削除の行が含まれないことを確認
        assert "🗑️ 削除" not in message

    def test_format_error_message_basic(self):
        """基本的なエラーメッセージのフォーマットテスト"""
        formatter = MessageFormatter()

        error_message = formatter.format_error_message(
            "connection_error", "Failed to connect to API", "test-source"
        )

        # 必要な要素が含まれていることを確認
        assert "🏮 Okina（翁）からのお知らせ" in error_message
        assert "🔍 ソース: test-source" in error_message
        assert "⚠️ 問題が発生しましたが、監視は継続しています" in error_message
        assert "種類: connection_error" in error_message
        assert "詳細: Failed to connect to API" in error_message
        assert "翁は静かに見守り続けます" in error_message


class TestSlackNotifier:
    """SlackNotifierクラスのテスト"""

    @patch("okina.notification.requests.post")
    def test_send_success(self, mock_post):
        """Slack通知の成功テスト"""
        # モックの設定
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        notifier = SlackNotifier("https://hooks.slack.com/test", "#test")
        result = notifier.send("Test message")

        assert result is True
        mock_post.assert_called_once()

        # 呼び出し引数の確認
        call_args = mock_post.call_args
        assert call_args[1]["json"]["text"] == "Test message"
        assert call_args[1]["json"]["channel"] == "#test"
        assert call_args[1]["json"]["username"] == "Okina（翁）"
        assert call_args[1]["json"]["icon_emoji"] == ":older_man:"

    @patch("okina.notification.requests.post")
    def test_send_failure(self, mock_post):
        """Slack通知の失敗テスト"""
        # モックの設定（エラーレスポンス）
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        notifier = SlackNotifier("https://hooks.slack.com/test", "#test")
        result = notifier.send("Test message")

        assert result is False


class TestNotificationManager:
    """NotificationManagerクラスのテスト"""

    def test_initialization_without_config(self):
        """設定なしでの初期化テスト"""
        manager = NotificationManager()

        assert manager.formatter is not None
        assert len(manager.notifiers) == 0

    @patch.dict("os.environ", {"TEST_WEBHOOK": "https://hooks.slack.com/test"})
    def test_initialization_with_slack_config(self):
        """Slack設定ありでの初期化テスト"""
        config = {"slack": {"webhook_url": "env:TEST_WEBHOOK", "channel": "#alerts"}}

        manager = NotificationManager(config)

        assert "slack" in manager.notifiers
        assert manager.notifiers["slack"].channel == "#alerts"

    @patch("okina.notification.SlackNotifier.send")
    def test_send_change_notification_success(self, mock_send):
        """変化通知の成功テスト"""
        mock_send.return_value = True

        config = {
            "slack": {"webhook_url": "https://hooks.slack.com/test", "channel": "#test"}
        }

        manager = NotificationManager(config)
        changes = {"added": 2, "changed": 1, "removed": 0}

        result = manager.send_change_notification(changes, "test-source")

        assert result is True
        mock_send.assert_called_once()

    def test_send_change_notification_no_changes(self):
        """変化なしの場合の通知テスト（静かに見守る）"""
        manager = NotificationManager()
        no_changes = {"added": 0, "changed": 0, "removed": 0}

        # 変化がない場合はTrueを返す（静かに見守る）
        result = manager.send_change_notification(no_changes, "test-source")
        assert result is True

    @patch("okina.notification.SlackNotifier.send")
    def test_continuity_on_partial_failure(self, mock_send):
        """一部失敗時の継続性テスト"""
        # 最初の呼び出しは失敗、2回目は成功をシミュレート
        mock_send.side_effect = [False, True]

        config = {
            "slack": {
                "webhook_url": "https://hooks.slack.com/test1",
                "channel": "#test1",
            }
        }

        manager = NotificationManager(config)

        # 複数の通知プラットフォームをシミュレート
        manager.notifiers["slack2"] = SlackNotifier(
            "https://hooks.slack.com/test2", "#test2"
        )

        changes = {"added": 1, "changed": 0, "removed": 0}
        result = manager.send_change_notification(changes, "test-source")

        # 一部成功すれば翁らしくTrueを返す
        assert result is True


# プロパティベーステスト用のマーカー
pytestmark = pytest.mark.okina


class TestCoverageImprovement:
    """カバレッジ向上のための追加テスト"""

    @pytest.mark.okina
    def test_format_change_message_with_all_change_types(self):
        """全ての変化タイプを含むメッセージのフォーマットテスト"""
        formatter = MessageFormatter()
        changes = {"added": 3, "changed": 2, "removed": 1}
        
        message = formatter.format_change_message(changes, "test-source")
        
        # 全ての変化タイプが含まれることを確認
        assert "✨ 新規追加: 3件" in message
        assert "🔄 内容変更: 2件" in message
        assert "🗑️ 削除: 1件" in message
        assert "🏮 Okina（翁）からのお知らせ" in message

    @pytest.mark.okina
    def test_slack_notifier_http_error_handling(self):
        """SlackNotifierのHTTPエラーハンドリングテスト"""
        notifier = SlackNotifier("https://hooks.slack.com/test", "#test")
        
        # HTTPエラーレスポンスをモック
        with patch("requests.post") as mock_post:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_post.return_value = mock_response
            
            result = notifier.send("Test message")
            
            assert result is False

    @pytest.mark.okina
    def test_slack_notifier_exception_handling(self):
        """SlackNotifierの例外ハンドリングテスト"""
        notifier = SlackNotifier("https://hooks.slack.com/test", "#test")
        
        # 例外を発生させる
        with patch("requests.post", side_effect=Exception("Network error")):
            result = notifier.send("Test message")
            
            assert result is False

    @pytest.mark.okina
    def test_notification_manager_error_scenarios(self):
        """NotificationManagerのエラーシナリオテスト"""
        config = {
            "slack": {
                "webhook_url": "https://hooks.slack.com/test",
                "channel": "#test"
            }
        }
        manager = NotificationManager(config)
        
        # 通知送信失敗をモック
        with patch.object(manager.notifiers["slack"], "send", return_value=False):
            result = manager.send_change_notification({}, "test-source")
            
            # 失敗しても継続性を保つ（翁らしい振る舞い）
            assert result is not None

    @pytest.mark.okina
    def test_notification_manager_send_change_exception(self):
        """NotificationManagerのsend_change_notificationで例外が発生した場合のテスト"""
        config = {
            "slack": {
                "webhook_url": "https://hooks.slack.com/test",
                "channel": "#test"
            }
        }
        manager = NotificationManager(config)
        
        # MessageFormatterで例外を発生させる
        with patch.object(manager.formatter, "format_change_message", 
                         side_effect=Exception("Format error")):
            result = manager.send_change_notification(
                {"added": 1}, "test-source"
            )
            
            # 例外が発生しても翁らしく継続性を保つ
            assert result is False

    @pytest.mark.okina
    def test_notification_manager_send_error_notification(self):
        """NotificationManagerのsend_error_notificationテスト"""
        config = {
            "slack": {
                "webhook_url": "https://hooks.slack.com/test",
                "channel": "#test"
            }
        }
        manager = NotificationManager(config)
        
        with patch.object(manager.notifiers["slack"], "send", return_value=True):
            result = manager.send_error_notification(
                "TestError", "Test error message", "test-source"
            )
            
            assert result is True

    @pytest.mark.okina
    def test_notification_manager_send_to_all_platforms(self):
        """NotificationManagerの_send_to_all_platformsテスト"""
        config = {
            "slack": {
                "webhook_url": "https://hooks.slack.com/test",
                "channel": "#test"
            }
        }
        manager = NotificationManager(config)
        
        with patch.object(manager.notifiers["slack"], "send", return_value=True):
            # プライベートメソッドを直接テスト
            result = manager._send_to_all_platforms("Test message")
            
            assert result is True