#!/usr/bin/env python3
"""
通知システム - 翁らしい静かで簡潔な通知

このモジュールはOkinaプロジェクトの一部として、
変化検知結果を複数のプラットフォームに翁らしく通知する機能を提供します。

Author: kamonabe
Created: 2026-01-06
"""

import logging
import os
from typing import Dict, Optional, Any
import requests
from datetime import datetime

# プロジェクト内インポート
from okina.exceptions import OkinaError

# ロガー設定
logger = logging.getLogger(__name__)


class NotificationError(OkinaError):
    """
    通知システム固有のエラー

    このクラスは通知システムの処理中に発生する
    特定のエラー状況を表現します。
    """

    pass


class MessageFormatter:
    """
    翁らしいメッセージフォーマッター

    このクラスは変化検知結果を翁らしい静かで簡潔なメッセージに
    フォーマットする機能を提供します。

    翁らしさの原則:
    - 静かで簡潔
    - 判断的でない事実ベース
    - 控えめで謙虚な表現
    - 人間の判断に委ねる姿勢

    Example:
        >>> formatter = MessageFormatter()
        >>> changes = {"added": 2, "changed": 1, "removed": 0}
        >>> message = formatter.format_change_message(changes, "fortinet-docs")
        >>> print(message)
        🏮 Okina（翁）からのお知らせ
        ✨ 新規追加: 2件
        🔄 内容変更: 1件
        詳細は okina history で確認できます
    """

    def __init__(self) -> None:
        """MessageFormatterを初期化"""
        self._message_templates = {
            "header": "🏮 Okina（翁）からのお知らせ",
            "date_format": "%Y-%m-%d %H:%M:%S",
            "footer": "詳細は okina history で確認できます",
        }

        logger.debug("MessageFormatter initialized with okina-style templates")

    def format_change_message(
        self,
        changes: Dict[str, int],
        source: str,
        timestamp: Optional[datetime] = None,
    ) -> str:
        """
        変化検知結果を翁らしいメッセージにフォーマット

        Args:
            changes (Dict[str, int]): 変化の統計
                {"added": N, "changed": N, "removed": N}
            source (str): データソース名
            timestamp (Optional[datetime]): タイムスタンプ

        Returns:
            str: 翁らしい静かで簡潔なメッセージ

        Example:
            >>> formatter = MessageFormatter()
            >>> changes = {"added": 2, "changed": 1, "removed": 0}
            >>> message = formatter.format_change_message(
            ...     changes, "fortinet-docs"
            ... )
            >>> assert "🏮 Okina（翁）からのお知らせ" in message
        """
        if not changes or all(count == 0 for count in changes.values()):
            # 変化がない場合は静かに見守る（通知しない）
            return ""

        timestamp = timestamp or datetime.now()

        # 翁らしい静かで簡潔なメッセージを構築
        lines = [
            self._message_templates["header"],
            f"📅 {timestamp.strftime(self._message_templates['date_format'])}",
            f"🔍 ソース: {source}",
        ]

        # 変化の内容を事実ベースで記載
        if changes.get("added", 0) > 0:
            lines.append(f"✨ 新規追加: {changes['added']}件")

        if changes.get("changed", 0) > 0:
            lines.append(f"🔄 内容変更: {changes['changed']}件")

        if changes.get("removed", 0) > 0:
            lines.append(f"🗑️ 削除: {changes['removed']}件")

        lines.append("")
        lines.append(self._message_templates["footer"])

        return "\n".join(lines)

    def format_error_message(
        self, error_type: str, error_message: str, source: Optional[str] = None
    ) -> str:
        """
        エラーを翁らしいメッセージにフォーマット

        翁らしいエラーハンドリング:
        - 継続性を重視
        - 過度に警告しない
        - 静かに記録

        Args:
            error_type (str): エラーの種類
            error_message (str): エラーメッセージ
            source (Optional[str]): エラーが発生したソース

        Returns:
            str: 翁らしい控えめなエラーメッセージ
        """
        timestamp = datetime.now()

        lines = [
            self._message_templates["header"],
            f"📅 {timestamp.strftime(self._message_templates['date_format'])}",
        ]

        if source:
            lines.append(f"🔍 ソース: {source}")

        lines.extend(
            [
                "",
                "⚠️ 問題が発生しましたが、監視は継続しています",
                f"種類: {error_type}",
                f"詳細: {error_message}",
                "",
                "翁は静かに見守り続けます",
            ]
        )

        return "\n".join(lines)


class SlackNotifier:
    """
    Slack通知クラス

    Webhook URLを使用してSlackに翁らしいメッセージを送信します。
    """

    def __init__(
        self, webhook_url: str, channel: str = "#alerts", username: str = "Okina（翁）"
    ):
        """
        SlackNotifierを初期化

        Args:
            webhook_url (str): SlackのWebhook URL
            channel (str): 送信先チャンネル
            username (str): 送信者名
        """
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username

        logger.debug(f"SlackNotifier initialized for channel {channel}")

    def send(self, message: str) -> bool:
        """
        Slackにメッセージを送信

        Args:
            message (str): 送信するメッセージ

        Returns:
            bool: 送信成功時True、失敗時False
        """
        try:
            payload = {
                "channel": self.channel,
                "username": self.username,
                "text": message,
                "icon_emoji": ":older_man:",  # 翁の絵文字
            }

            response = requests.post(self.webhook_url, json=payload, timeout=30)

            if response.status_code == 200:
                logger.info(f"Slack notification sent successfully to {self.channel}")
                return True
            else:
                logger.warning(f"Slack notification failed: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")
            return False


class NotificationManager:
    """
    通知管理クラス

    このクラスは複数の通知プラットフォームを統合管理し、
    翁らしい一貫したインターフェースで通知送信を行います。

    翁らしい設計原則:
    - 継続性を重視（一部失敗でも処理継続）
    - 静かなエラーハンドリング
    - 環境変数による安全な設定管理

    Attributes:
        formatter (MessageFormatter): メッセージフォーマッター
        notifiers (Dict[str, Any]): 通知プラットフォーム一覧

    Example:
        >>> config = {"slack": {"webhook_url": "env:OKINA_SLACK_WEBHOOK"}}
        >>> manager = NotificationManager(config)
        >>> changes = {"added": 2, "changed": 1}
        >>> success = manager.send_change_notification(changes, "fortinet-docs")
        >>> assert success
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        NotificationManagerを初期化

        Args:
            config (Optional[Dict[str, Any]]): 通知設定辞書
                例: {
                    "slack": {
                        "webhook_url": "env:OKINA_SLACK_WEBHOOK",
                        "channel": "#alerts"
                    }
                }

        Raises:
            NotificationError: 設定が無効な場合
        """
        self.config = config or {}
        self.formatter = MessageFormatter()
        self.notifiers: Dict[str, Any] = {}

        # 通知プラットフォームを初期化
        self._initialize_notifiers()

        logger.info(
            f"NotificationManager initialized with {len(self.notifiers)} notifiers"
        )

    def send_change_notification(
        self, changes: Dict[str, int], source: str, timestamp: Optional[datetime] = None
    ) -> bool:
        """
        変化検知結果を通知

        Args:
            changes (Dict[str, int]): 変化の統計
            source (str): データソース名
            timestamp (Optional[datetime]): タイムスタンプ

        Returns:
            bool: 全ての通知が成功した場合True

        Example:
            >>> manager = NotificationManager()
            >>> changes = {"added": 2, "changed": 1, "removed": 0}
            >>> success = manager.send_change_notification(changes, "fortinet-docs")
        """
        try:
            # 翁らしいメッセージを生成
            message = self.formatter.format_change_message(changes, source, timestamp)

            if not message:
                # 変化がない場合は静かに見守る
                logger.debug("No changes detected, staying quiet like okina")
                return True

            # 全ての通知プラットフォームに送信
            return self._send_to_all_platforms(message)

        except Exception as e:
            logger.error(f"Error in send_change_notification: {e}")
            # 翁らしく、エラーでも継続性を保つ
            return False

    def send_error_notification(
        self, error_type: str, error_message: str, source: Optional[str] = None
    ) -> bool:
        """
        エラーを通知

        Args:
            error_type (str): エラーの種類
            error_message (str): エラーメッセージ
            source (Optional[str]): エラーが発生したソース

        Returns:
            bool: 通知送信の成功可否
        """
        try:
            message = self.formatter.format_error_message(
                error_type, error_message, source
            )
            return self._send_to_all_platforms(message)

        except Exception as e:
            logger.error(f"Error in send_error_notification: {e}")
            return False

    def _initialize_notifiers(self) -> None:
        """通知プラットフォームを初期化"""
        if "slack" in self.config:
            slack_config = self.config["slack"]
            webhook_url = self._resolve_env_var(slack_config.get("webhook_url", ""))

            if webhook_url:
                self.notifiers["slack"] = SlackNotifier(
                    webhook_url=webhook_url,
                    channel=slack_config.get("channel", "#alerts"),
                    username=slack_config.get("username", "Okina（翁）"),
                )
                logger.debug("Slack notifier initialized")

    def _resolve_env_var(self, value: str) -> str:
        """
        環境変数を解決

        Args:
            value (str): "env:VAR_NAME" 形式または直接値

        Returns:
            str: 解決された値
        """
        if value.startswith("env:"):
            env_var = value[4:]  # "env:" を除去
            resolved = os.getenv(env_var, "")
            if not resolved:
                logger.warning(f"Environment variable {env_var} not found")
            return resolved
        return value

    def _send_to_all_platforms(self, message: str) -> bool:
        """
        全ての通知プラットフォームにメッセージを送信

        翁らしい継続性: 一部が失敗しても他は継続

        Args:
            message (str): 送信するメッセージ

        Returns:
            bool: 少なくとも1つの通知が成功した場合True
        """
        if not self.notifiers:
            logger.warning("No notifiers configured")
            return False

        success_count = 0

        for platform, notifier in self.notifiers.items():
            try:
                if notifier.send(message):
                    success_count += 1
                    logger.debug(f"Notification sent successfully to {platform}")
                else:
                    logger.warning(f"Notification failed for {platform}")
            except Exception as e:
                logger.error(f"Error sending notification to {platform}: {e}")

        # 翁らしく、少なくとも1つ成功すれば良しとする
        return success_count > 0

    def __str__(self) -> str:
        """文字列表現を返す"""
        return f"NotificationManager(platforms={list(self.notifiers.keys())})"

    def __repr__(self) -> str:
        """開発者向け文字列表現を返す"""
        return f"NotificationManager(notifiers={len(self.notifiers)})"


# モジュールレベルの定数
DEFAULT_TIMEOUT = 30
MAX_RETRY_COUNT = 3


if __name__ == "__main__":
    # モジュール単体テスト用のコード
    import doctest

    # doctestを実行
    doctest.testmod(verbose=True)

    # 簡単な動作確認
    try:
        formatter = MessageFormatter()
        changes = {"added": 2, "changed": 1, "removed": 0}
        message = formatter.format_change_message(changes, "test-source")
        print("Test successful:")
        print(message)
    except Exception as e:
        print(f"Test failed: {e}")
