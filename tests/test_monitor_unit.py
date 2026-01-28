#!/usr/bin/env python3
"""
変化監視システムのユニットテスト

このモジュールは変化監視システムの各コンポーネントの
ユニットテストを提供します。

Author: kamonabe
Created: 2026-01-28
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from okina.monitor import (
    ChangeMonitor,
    ConfigManager,
    DataWatcher,
    ProcessController,
    ErrorHandler,
    MonitorError,
)
from okina.analyzer import DiffAnalyzer
from okina.notification import NotificationManager


class TestConfigManager:
    """ConfigManagerクラスのユニットテスト"""

    def test_load_config_success(self, tmp_path):
        """正常な設定ファイルの読み込み"""
        config_file = tmp_path / "settings.yml"
        config_content = """
input:
  data_directory: "data/input"
  file_pattern: "*.jsonl"
storage:
  history_directory: "data/history"
  max_history_days: 30
notifications:
  slack:
    enabled: true
    webhook_url: "env:OKINA_SLACK_WEBHOOK"
"""
        config_file.write_text(config_content, encoding="utf-8")

        manager = ConfigManager()
        config = manager.load_config(str(config_file))

        assert "input" in config
        assert "storage" in config
        assert "notifications" in config
        assert config["input"]["data_directory"] == "data/input"

    def test_load_config_file_not_found(self):
        """存在しない設定ファイルの読み込み"""
        manager = ConfigManager()

        with pytest.raises(MonitorError, match="設定ファイルが見つかりません"):
            manager.load_config("nonexistent.yml")

    def test_load_config_invalid_yaml(self, tmp_path):
        """不正なYAML形式の設定ファイル"""
        config_file = tmp_path / "invalid.yml"
        config_file.write_text("invalid: yaml: content:", encoding="utf-8")

        manager = ConfigManager()

        with pytest.raises(MonitorError, match="設定ファイルの形式が不正です"):
            manager.load_config(str(config_file))

    def test_validate_config_missing_section(self):
        """必須セクションが不足している設定"""
        manager = ConfigManager()

        config = {"input": {"data_directory": "data/input"}}

        with pytest.raises(MonitorError, match="必須設定セクション"):
            manager.validate_config(config)

    def test_validate_config_missing_data_directory(self):
        """data_directoryが不足している設定"""
        manager = ConfigManager()

        config = {
            "input": {},
            "storage": {"history_directory": "data/history"},
            "notifications": {},
        }

        with pytest.raises(MonitorError, match="data_directory が設定されていません"):
            manager.validate_config(config)

    def test_validate_config_success(self):
        """正常な設定の検証"""
        manager = ConfigManager()

        config = {
            "input": {"data_directory": "data/input"},
            "storage": {"history_directory": "data/history"},
            "notifications": {"slack": {"enabled": True}},
        }

        result = manager.validate_config(config)
        assert result is True


class TestDataWatcher:
    """DataWatcherクラスのユニットテスト"""

    def test_find_source_files_success(self, tmp_path):
        """ソースファイルの検出（成功）"""
        # テストファイルを作成
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        (input_dir / "fortinet.jsonl").write_text("test", encoding="utf-8")
        (input_dir / "cisco.jsonl").write_text("test", encoding="utf-8")
        (input_dir / "vmware.jsonl").write_text("test", encoding="utf-8")

        watcher = DataWatcher()
        files = watcher.find_source_files(str(input_dir), "*.jsonl")

        assert len(files) == 3
        assert any("fortinet.jsonl" in f for f in files)
        assert any("cisco.jsonl" in f for f in files)
        assert any("vmware.jsonl" in f for f in files)

    def test_find_source_files_directory_not_found(self):
        """存在しないディレクトリの監視"""
        watcher = DataWatcher()

        with pytest.raises(MonitorError, match="データディレクトリが見つかりません"):
            watcher.find_source_files("nonexistent_dir", "*.jsonl")

    def test_find_source_files_empty_directory(self, tmp_path):
        """空ディレクトリの監視"""
        input_dir = tmp_path / "empty"
        input_dir.mkdir()

        watcher = DataWatcher()
        files = watcher.find_source_files(str(input_dir), "*.jsonl")

        assert len(files) == 0

    def test_extract_source_name(self):
        """ソース名の抽出"""
        watcher = DataWatcher()

        assert watcher.extract_source_name("data/input/fortinet.jsonl") == "fortinet"
        assert watcher.extract_source_name("/path/to/cisco.jsonl") == "cisco"
        assert watcher.extract_source_name("vmware.jsonl") == "vmware"


class TestProcessController:
    """ProcessControllerクラスのユニットテスト"""

    def test_process_source_with_changes(self, tmp_path):
        """変化があるソースの処理"""
        # テストデータを作成
        test_file = tmp_path / "test.jsonl"
        test_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T10:00:00+09:00",
            }
        ]

        with test_file.open("w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # モックを作成
        history_dir = tmp_path / "history"
        history_dir.mkdir()

        diff_analyzer = DiffAnalyzer({"storage": {"history_directory": str(history_dir)}})
        notification_manager = Mock(spec=NotificationManager)
        notification_manager.send_change_notification.return_value = True

        controller = ProcessController(diff_analyzer, notification_manager)

        # 処理を実行
        result = controller.process_source("test", str(test_file))

        assert result["success"] is True
        assert result["source_name"] == "test"
        assert "diff_result" in result
        assert result["notification_sent"] is True

        # 通知が呼び出されたことを確認
        notification_manager.send_change_notification.assert_called_once()

    def test_process_source_no_changes(self, tmp_path):
        """変化がないソースの処理"""
        # 初回データを作成
        test_file = tmp_path / "test.jsonl"
        test_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T10:00:00+09:00",
            }
        ]

        with test_file.open("w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        history_dir = tmp_path / "history"
        history_dir.mkdir()

        diff_analyzer = DiffAnalyzer({"storage": {"history_directory": str(history_dir)}})
        notification_manager = Mock(spec=NotificationManager)
        notification_manager.send_change_notification.return_value = True

        controller = ProcessController(diff_analyzer, notification_manager)

        # 初回実行（全て新規追加）
        result1 = controller.process_source("test", str(test_file))
        assert result1["success"] is True
        assert result1["notification_sent"] is True  # 初回は新規追加として通知される

        # モックをリセット
        notification_manager.reset_mock()

        # 2回目実行（変化なし）
        result2 = controller.process_source("test", str(test_file))

        assert result2["success"] is True
        assert result2["notification_sent"] is False

        # 2回目は通知が呼び出されていないことを確認
        notification_manager.send_change_notification.assert_not_called()

    def test_process_source_analyzer_error(self, tmp_path):
        """差分抽出エラー時の処理"""
        diff_analyzer = Mock(spec=DiffAnalyzer)
        diff_analyzer.analyze_changes.side_effect = Exception("Test error")

        notification_manager = Mock(spec=NotificationManager)

        controller = ProcessController(diff_analyzer, notification_manager)

        result = controller.process_source("test", "nonexistent.jsonl")

        assert result["success"] is False
        assert "error" in result

        # 異常通知が呼び出されたことを確認
        notification_manager.send_error_notification.assert_called_once()


class TestErrorHandler:
    """ErrorHandlerクラスのユニットテスト"""

    def test_handle_error_with_source(self):
        """ソース指定ありのエラー処理"""
        notification_manager = Mock(spec=NotificationManager)
        handler = ErrorHandler(notification_manager)

        handler.handle_error("テストエラー", "エラーメッセージ", source="test-source")

        notification_manager.send_error_notification.assert_called_once_with(
            "テストエラー", "エラーメッセージ", "test-source"
        )

    def test_handle_error_without_source(self):
        """ソース指定なしのエラー処理"""
        notification_manager = Mock(spec=NotificationManager)
        handler = ErrorHandler(notification_manager)

        handler.handle_error("テストエラー", "エラーメッセージ")

        notification_manager.send_error_notification.assert_called_once_with(
            "テストエラー", "エラーメッセージ", None
        )

    def test_handle_error_notification_failure(self):
        """通知送信失敗時のエラー処理"""
        notification_manager = Mock(spec=NotificationManager)
        notification_manager.send_error_notification.side_effect = Exception(
            "Notification failed"
        )

        handler = ErrorHandler(notification_manager)

        # 例外が発生しないことを確認
        handler.handle_error("テストエラー", "エラーメッセージ")


class TestChangeMonitor:
    """ChangeMonitorクラスのユニットテスト"""

    def test_initialization(self, tmp_path):
        """初期化テスト"""
        config_file = tmp_path / "settings.yml"
        config_content = """
input:
  data_directory: "data/input"
storage:
  history_directory: "data/history"
notifications:
  slack:
    enabled: false
"""
        config_file.write_text(config_content, encoding="utf-8")

        monitor = ChangeMonitor(str(config_file))

        assert monitor.config is not None
        assert monitor.config_manager is not None
        assert monitor.data_watcher is not None
        assert monitor.diff_analyzer is not None
        assert monitor.notification_manager is not None
        assert monitor.process_controller is not None
        assert monitor.error_handler is not None

    def test_watch_changes_no_files(self, tmp_path):
        """ファイルなしの変化監視"""
        # 設定ファイルを作成
        config_file = tmp_path / "settings.yml"
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        config_content = f"""
input:
  data_directory: "{input_dir}"
storage:
  history_directory: "{tmp_path / 'history'}"
notifications:
  slack:
    enabled: false
"""
        config_file.write_text(config_content, encoding="utf-8")

        monitor = ChangeMonitor(str(config_file))
        result = monitor.watch_changes()

        assert result["success"] is False
        assert result["sources_processed"] == 0
        assert len(result["errors"]) == 0  # エラーハンドラーで処理される

    def test_watch_changes_with_files(self, tmp_path):
        """ファイルありの変化監視"""
        # 設定ファイルを作成
        config_file = tmp_path / "settings.yml"
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        # テストデータを作成
        test_file = input_dir / "test.jsonl"
        test_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T10:00:00+09:00",
            }
        ]

        with test_file.open("w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        config_content = f"""
input:
  data_directory: "{input_dir}"
storage:
  history_directory: "{history_dir}"
notifications:
  slack:
    enabled: false
"""
        config_file.write_text(config_content, encoding="utf-8")

        monitor = ChangeMonitor(str(config_file))
        result = monitor.watch_changes()

        assert result["success"] is True
        assert result["sources_processed"] == 1
        assert result["sources_with_changes"] == 1
