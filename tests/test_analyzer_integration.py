#!/usr/bin/env python3
"""
差分抽出システムの統合テスト

このモジュールは差分抽出システム全体の統合テストを提供します。

Author: kamonabe
Created: 2026-01-28
"""

import json
import pytest
from pathlib import Path

from okina.analyzer import DiffAnalyzer, AnalyzerError


class TestDiffAnalyzerIntegration:
    """DiffAnalyzer統合テスト"""

    def test_end_to_end_diff_analysis(self, tmp_path):
        """エンドツーエンドの差分分析フロー"""
        # ディレクトリ構成を作成
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        # 初回実行: 3件のデータ
        first_data = [
            {
                "schema": "okina.item.v1",
                "source": "fortinet",
                "id": "fortinet:fortios:7.6.4:release",
                "type": "release",
                "title": "FortiOS 7.6.4",
                "url": "https://docs.fortinet.com/7.6.4",
                "observed_at": "2026-01-28T10:00:00+09:00",
                "version": "7.6.4",
            },
            {
                "schema": "okina.item.v1",
                "source": "fortinet",
                "id": "fortinet:fortios:7.6.5:release",
                "type": "release",
                "title": "FortiOS 7.6.5",
                "url": "https://docs.fortinet.com/7.6.5",
                "observed_at": "2026-01-28T10:00:00+09:00",
                "version": "7.6.5",
            },
            {
                "schema": "okina.item.v1",
                "source": "fortinet",
                "id": "fortinet:fortios:7.6.6:release",
                "type": "release",
                "title": "FortiOS 7.6.6",
                "url": "https://docs.fortinet.com/7.6.6",
                "observed_at": "2026-01-28T10:00:00+09:00",
                "version": "7.6.6",
            },
        ]

        first_file = input_dir / "fortinet_first.jsonl"
        with first_file.open("w", encoding="utf-8") as f:
            for item in first_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 設定
        settings = {
            "storage": {"history_directory": str(history_dir), "max_history_days": 30},
            "comparison": {"use_content_hash": False},
        }

        analyzer = DiffAnalyzer(settings)

        # 初回実行
        result1 = analyzer.analyze_changes("fortinet", str(first_file))

        assert result1["summary"]["total_current"] == 3
        assert result1["summary"]["added_count"] == 3
        assert result1["summary"]["removed_count"] == 0
        assert result1["summary"]["changed_count"] == 0

        # 2回目実行: 新規追加1件、削除1件、変更1件
        second_data = [
            {
                "schema": "okina.item.v1",
                "source": "fortinet",
                "id": "fortinet:fortios:7.6.5:release",
                "type": "release",
                "title": "FortiOS 7.6.5",
                "url": "https://docs.fortinet.com/7.6.5",
                "observed_at": "2026-01-28T11:00:00+09:00",
                "version": "7.6.5",
            },
            {
                "schema": "okina.item.v1",
                "source": "fortinet",
                "id": "fortinet:fortios:7.6.6:release",
                "type": "release",
                "title": "FortiOS 7.6.6 Updated",  # タイトル変更
                "url": "https://docs.fortinet.com/7.6.6",
                "observed_at": "2026-01-28T11:00:00+09:00",
                "version": "7.6.6",
            },
            {
                "schema": "okina.item.v1",
                "source": "fortinet",
                "id": "fortinet:fortios:7.6.7:release",  # 新規追加
                "type": "release",
                "title": "FortiOS 7.6.7",
                "url": "https://docs.fortinet.com/7.6.7",
                "observed_at": "2026-01-28T11:00:00+09:00",
                "version": "7.6.7",
            },
        ]

        second_file = input_dir / "fortinet_second.jsonl"
        with second_file.open("w", encoding="utf-8") as f:
            for item in second_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 2回目実行
        result2 = analyzer.analyze_changes("fortinet", str(second_file))

        assert result2["summary"]["total_current"] == 3
        assert result2["summary"]["added_count"] == 1
        assert result2["summary"]["removed_count"] == 1
        assert result2["summary"]["changed_count"] == 1

        # 新規追加の確認
        assert result2["added"][0]["id"] == "fortinet:fortios:7.6.7:release"

        # 削除の確認
        assert result2["removed"][0]["id"] == "fortinet:fortios:7.6.4:release"

        # 変更の確認
        assert result2["changed"][0]["id"] == "fortinet:fortios:7.6.6:release"
        assert any(
            change["field"] == "title" for change in result2["changed"][0]["changes"]
        )

    def test_multiple_source_processing(self, tmp_path):
        """複数ソースの独立処理"""
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        settings = {
            "storage": {"history_directory": str(history_dir)},
            "comparison": {"use_content_hash": False},
        }

        analyzer = DiffAnalyzer(settings)

        # ソース1: Fortinet
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

        fortinet_file = input_dir / "fortinet.jsonl"
        with fortinet_file.open("w", encoding="utf-8") as f:
            for item in fortinet_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # ソース2: Cisco
        cisco_data = [
            {
                "schema": "okina.item.v1",
                "source": "cisco",
                "id": "cisco:ios-xe:17.12.01:advisory",
                "type": "advisory",
                "title": "Cisco IOS XE 17.12.01",
                "url": "https://www.cisco.com/17.12.01",
                "observed_at": "2026-01-28T10:00:00+09:00",
            }
        ]

        cisco_file = input_dir / "cisco.jsonl"
        with cisco_file.open("w", encoding="utf-8") as f:
            for item in cisco_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 各ソースを独立処理
        result_fortinet = analyzer.analyze_changes("fortinet", str(fortinet_file))
        result_cisco = analyzer.analyze_changes("cisco", str(cisco_file))

        # 各ソースが独立して処理されている
        assert result_fortinet["summary"]["added_count"] == 1
        assert result_cisco["summary"]["added_count"] == 1

        # 履歴ファイルが独立して作成されている
        fortinet_history = list(history_dir.glob("fortinet_*.json"))
        cisco_history = list(history_dir.glob("cisco_*.json"))

        assert len(fortinet_history) == 1
        assert len(cisco_history) == 1

    def test_content_hash_optimization(self, tmp_path):
        """content_hash最適化の動作確認"""
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        # 初回データ（content_hashあり）
        first_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T10:00:00+09:00",
                "content_hash": "abc123",
            }
        ]

        first_file = input_dir / "test_first.jsonl"
        with first_file.open("w", encoding="utf-8") as f:
            for item in first_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        settings = {
            "storage": {"history_directory": str(history_dir)},
            "comparison": {"use_content_hash": True},
        }

        analyzer = DiffAnalyzer(settings)

        # 初回実行
        analyzer.analyze_changes("test", str(first_file))

        # 2回目: content_hashが同じ（変更なし）
        second_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T11:00:00+09:00",  # 時刻のみ変更
                "content_hash": "abc123",  # ハッシュ値は同じ
            }
        ]

        second_file = input_dir / "test_second.jsonl"
        with second_file.open("w", encoding="utf-8") as f:
            for item in second_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        result = analyzer.analyze_changes("test", str(second_file))

        # ハッシュ値が同じなので変更なし
        assert result["summary"]["changed_count"] == 0

        # 3回目: content_hashが異なる（変更あり）
        third_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1 Updated",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T12:00:00+09:00",
                "content_hash": "def456",  # ハッシュ値が変更
            }
        ]

        third_file = input_dir / "test_third.jsonl"
        with third_file.open("w", encoding="utf-8") as f:
            for item in third_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        result = analyzer.analyze_changes("test", str(third_file))

        # ハッシュ値が異なるので変更あり
        assert result["summary"]["changed_count"] == 1

    def test_error_handling_invalid_data(self, tmp_path):
        """不正データのエラーハンドリング"""
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        # ID重複データ
        duplicate_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T10:00:00+09:00",
            },
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",  # 重複
                "type": "release",
                "title": "Test 1 Duplicate",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T10:00:00+09:00",
            },
        ]

        test_file = input_dir / "duplicate.jsonl"
        with test_file.open("w", encoding="utf-8") as f:
            for item in duplicate_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        settings = {
            "storage": {"history_directory": str(history_dir)},
            "comparison": {"use_content_hash": False},
        }

        analyzer = DiffAnalyzer(settings)

        # ID重複エラーが発生
        with pytest.raises(AnalyzerError, match="ID重複が検出されました"):
            analyzer.analyze_changes("test", str(test_file))

    def test_history_persistence_on_success_only(self, tmp_path):
        """正常終了時のみ履歴が保存される"""
        input_dir = tmp_path / "input"
        history_dir = tmp_path / "history"
        input_dir.mkdir()
        history_dir.mkdir()

        settings = {
            "storage": {"history_directory": str(history_dir)},
            "comparison": {"use_content_hash": False},
        }

        analyzer = DiffAnalyzer(settings)

        # 正常なデータで実行
        valid_data = [
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

        valid_file = input_dir / "valid.jsonl"
        with valid_file.open("w", encoding="utf-8") as f:
            for item in valid_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        analyzer.analyze_changes("test", str(valid_file))

        # 履歴が保存されている
        history_files = list(history_dir.glob("test_*.json"))
        assert len(history_files) == 1

        # 不正なデータで実行（エラー発生）
        invalid_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T11:00:00+09:00",
            },
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",  # 重複
                "type": "release",
                "title": "Test 1 Duplicate",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T11:00:00+09:00",
            },
        ]

        invalid_file = input_dir / "invalid.jsonl"
        with invalid_file.open("w", encoding="utf-8") as f:
            for item in invalid_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        try:
            analyzer.analyze_changes("test", str(invalid_file))
        except AnalyzerError:
            pass

        # エラー時は履歴が更新されない（前回のまま）
        history_files = list(history_dir.glob("test_*.json"))
        assert len(history_files) == 1  # 増えていない
