#!/usr/bin/env python3
"""
変化監視システムの統合テスト

このモジュールは変化監視システム全体の統合テストを提供します。

Author: kamonabe
Created: 2026-01-28
"""

import json
import pytest
from pathlib import Path

from okina.monitor import ChangeMonitor, MonitorError


class TestChangeMonitorIntegration:
    """ChangeMonitor統合テスト"""

    def test_end_to_end_monitoring_flow(self, tmp_path):
        """エンドツーエンドの変化監視フロー"""
        # ディレクトリ構成を作成
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        # 設定ファイルを作成
        config_file = tmp_path / "settings.yml"
        config_content = f"""
input:
  data_directory: "{input_dir}"
  file_pattern: "*.jsonl"
storage:
  history_directory: "{history_dir}"
  max_history_days: 30
notifications:
  slack:
    enabled: false
"""
        config_file.write_text(config_content, encoding="utf-8")

        # 初回データを作成
        fortinet_file = input_dir / "fortinet.jsonl"
        fortinet_data = [
            {
                "schema": "okina.item.v1",
                "source": "fortinet",
                "id": "fortinet:fortios:7.6.6:release",
                "type": "release",
                "title": "FortiOS 7.6.6",
                "url": "https://docs.fortinet.com/7.6.6",
                "observed_at": "2026-01-28T10:00:00+09:00",
            }
        ]

        with fortinet_file.open("w", encoding="utf-8") as f:
            for item in fortinet_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 初回実行
        monitor = ChangeMonitor(str(config_file))
        success = monitor.run()

        assert success is True

        # 履歴ファイルが作成されたことを確認
        history_files = list(history_dir.glob("fortinet_*.json"))
        assert len(history_files) == 1

        # 2回目データを作成（変更あり）
        fortinet_data_updated = [
            {
                "schema": "okina.item.v1",
                "source": "fortinet",
                "id": "fortinet:fortios:7.6.6:release",
                "type": "release",
                "title": "FortiOS 7.6.6 Updated",  # タイトル変更
                "url": "https://docs.fortinet.com/7.6.6",
                "observed_at": "2026-01-28T11:00:00+09:00",
            },
            {
                "schema": "okina.item.v1",
                "source": "fortinet",
                "id": "fortinet:fortios:7.6.7:release",  # 新規追加
                "type": "release",
                "title": "FortiOS 7.6.7",
                "url": "https://docs.fortinet.com/7.6.7",
                "observed_at": "2026-01-28T11:00:00+09:00",
            },
        ]

        with fortinet_file.open("w", encoding="utf-8") as f:
            for item in fortinet_data_updated:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 2回目実行
        monitor2 = ChangeMonitor(str(config_file))
        result = monitor2.watch_changes()

        assert result["success"] is True
        assert result["sources_processed"] == 1
        assert result["sources_with_changes"] == 1
        assert result["total_changes"]["added"] == 1
        assert result["total_changes"]["changed"] == 1

    def test_multiple_source_processing(self, tmp_path):
        """複数ソースの独立処理"""
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        # 設定ファイルを作成
        config_file = tmp_path / "settings.yml"
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

        # 複数のソースファイルを作成
        sources = ["fortinet", "cisco", "vmware"]

        for source in sources:
            source_file = input_dir / f"{source}.jsonl"
            source_data = [
                {
                    "schema": "okina.item.v1",
                    "source": source,
                    "id": f"{source}:test:1.0:release",
                    "type": "release",
                    "title": f"{source.capitalize()} Test 1.0",
                    "url": f"https://{source}.com/1.0",
                    "observed_at": "2026-01-28T10:00:00+09:00",
                }
            ]

            with source_file.open("w", encoding="utf-8") as f:
                for item in source_data:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 実行
        monitor = ChangeMonitor(str(config_file))
        result = monitor.watch_changes()

        assert result["success"] is True
        assert result["sources_processed"] == 3
        assert result["sources_with_changes"] == 3

        # 各ソースの履歴ファイルが作成されたことを確認
        for source in sources:
            history_files = list(history_dir.glob(f"{source}_*.json"))
            assert len(history_files) == 1

    def test_error_handling_partial_failure(self, tmp_path):
        """部分的な失敗のエラーハンドリング"""
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        # 設定ファイルを作成
        config_file = tmp_path / "settings.yml"
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

        # 正常なファイルと不正なファイルを作成
        # 正常なファイル
        valid_file = input_dir / "valid.jsonl"
        valid_data = [
            {
                "schema": "okina.item.v1",
                "source": "valid",
                "id": "valid:test:1.0:release",
                "type": "release",
                "title": "Valid Test 1.0",
                "url": "https://valid.com/1.0",
                "observed_at": "2026-01-28T10:00:00+09:00",
            }
        ]

        with valid_file.open("w", encoding="utf-8") as f:
            for item in valid_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 不正なファイル（ID重複）
        invalid_file = input_dir / "invalid.jsonl"
        invalid_data = [
            {
                "schema": "okina.item.v1",
                "source": "invalid",
                "id": "invalid:test:1.0:release",
                "type": "release",
                "title": "Invalid Test 1.0",
                "url": "https://invalid.com/1.0",
                "observed_at": "2026-01-28T10:00:00+09:00",
            },
            {
                "schema": "okina.item.v1",
                "source": "invalid",
                "id": "invalid:test:1.0:release",  # 重複
                "type": "release",
                "title": "Invalid Test 1.0 Duplicate",
                "url": "https://invalid.com/1.0",
                "observed_at": "2026-01-28T10:00:00+09:00",
            },
        ]

        with invalid_file.open("w", encoding="utf-8") as f:
            for item in invalid_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 実行
        monitor = ChangeMonitor(str(config_file))
        result = monitor.watch_changes()

        # 部分的な成功
        assert result["sources_processed"] == 2
        assert len(result["errors"]) == 1

        # 正常なファイルの履歴は作成される
        valid_history = list(history_dir.glob("valid_*.json"))
        assert len(valid_history) == 1

        # 不正なファイルの履歴は作成されない
        invalid_history = list(history_dir.glob("invalid_*.json"))
        assert len(invalid_history) == 0

    def test_config_management_and_logging(self, tmp_path):
        """設定管理とログ記録の統合テスト"""
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        log_dir = tmp_path / "log"
        input_dir.mkdir()
        history_dir.mkdir()
        log_dir.mkdir()

        # 設定ファイルを作成
        config_file = tmp_path / "settings.yml"
        config_content = f"""
input:
  data_directory: "{input_dir}"
  file_pattern: "*.jsonl"
storage:
  history_directory: "{history_dir}"
  max_history_days: 30
notifications:
  slack:
    enabled: false
logging:
  level: "INFO"
  file: "{log_dir / 'okina.log'}"
"""
        config_file.write_text(config_content, encoding="utf-8")

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

        # 実行
        monitor = ChangeMonitor(str(config_file))
        success = monitor.run()

        assert success is True

        # 設定が正しく読み込まれたことを確認
        assert monitor.config["input"]["data_directory"] == str(input_dir)
        assert monitor.config["storage"]["history_directory"] == str(history_dir)

    def test_empty_directory_handling(self, tmp_path):
        """空ディレクトリの処理"""
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        # 設定ファイルを作成
        config_file = tmp_path / "settings.yml"
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

        # 実行（ファイルなし）
        monitor = ChangeMonitor(str(config_file))
        result = monitor.watch_changes()

        # データなし異常として処理される
        assert result["success"] is False
        assert result["sources_processed"] == 0

    def test_notification_integration(self, tmp_path):
        """通知システムとの統合テスト"""
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        # 設定ファイルを作成（通知無効）
        config_file = tmp_path / "settings.yml"
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

        # 実行
        monitor = ChangeMonitor(str(config_file))
        success = monitor.run()

        # 通知が無効でも処理は成功する
        assert success is True
