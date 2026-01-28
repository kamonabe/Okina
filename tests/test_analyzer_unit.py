#!/usr/bin/env python3
"""
差分抽出システムのユニットテスト

このモジュールは差分抽出システムの各コンポーネントの
ユニットテストを提供します。

Author: kamonabe
Created: 2026-01-28
"""

import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, mock_open

from okina.analyzer import (
    DiffAnalyzer,
    DataLoader,
    ComparisonEngine,
    HistoryManager,
    AnalyzerError,
)


class TestDataLoader:
    """DataLoaderクラスのユニットテスト"""

    def test_load_jsonl_success(self, tmp_path):
        """正常なJSONLファイルの読み込み"""
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
            },
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id2",
                "type": "release",
                "title": "Test 2",
                "url": "https://example.com/2",
                "observed_at": "2026-01-28T10:00:00+09:00",
            },
        ]

        with test_file.open("w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # テスト実行
        loader = DataLoader()
        result = loader.load_jsonl(str(test_file))

        # 検証
        assert len(result) == 2
        assert result[0]["id"] == "test:id1"
        assert result[1]["id"] == "test:id2"

    def test_load_jsonl_file_not_found(self):
        """存在しないファイルの読み込み"""
        loader = DataLoader()

        with pytest.raises(AnalyzerError, match="データファイルが見つかりません"):
            loader.load_jsonl("nonexistent.jsonl")

    def test_load_jsonl_invalid_json(self, tmp_path):
        """不正なJSON行を含むファイルの読み込み"""
        test_file = tmp_path / "invalid.jsonl"
        test_file.write_text(
            '{"schema": "okina.item.v1", "source": "test", "id": "test:id1", '
            '"type": "release", "title": "Test 1", "url": "https://example.com/1", '
            '"observed_at": "2026-01-28T10:00:00+09:00"}\n'
            'invalid json line\n'
            '{"schema": "okina.item.v1", "source": "test", "id": "test:id2", '
            '"type": "release", "title": "Test 2", "url": "https://example.com/2", '
            '"observed_at": "2026-01-28T10:00:00+09:00"}\n',
            encoding="utf-8",
        )

        loader = DataLoader()
        result = loader.load_jsonl(str(test_file))

        # 不正な行はスキップされ、正常な2行のみ読み込まれる
        assert len(result) == 2

    def test_load_jsonl_missing_required_field(self, tmp_path):
        """必須フィールドが不足しているデータの読み込み"""
        test_file = tmp_path / "missing_field.jsonl"
        test_file.write_text(
            '{"schema": "okina.item.v1", "source": "test", "id": "test:id1"}\n'
            '{"schema": "okina.item.v1", "source": "test", "id": "test:id2", '
            '"type": "release", "title": "Test 2", "url": "https://example.com/2", '
            '"observed_at": "2026-01-28T10:00:00+09:00"}\n',
            encoding="utf-8",
        )

        loader = DataLoader()
        result = loader.load_jsonl(str(test_file))

        # 必須フィールド不足の行はスキップされる
        assert len(result) == 1
        assert result[0]["id"] == "test:id2"

    def test_check_id_uniqueness_success(self):
        """ID一意性チェック（成功）"""
        loader = DataLoader()
        data = [
            {"id": "test:id1", "title": "Test 1"},
            {"id": "test:id2", "title": "Test 2"},
            {"id": "test:id3", "title": "Test 3"},
        ]

        result = loader.check_id_uniqueness(data)
        assert result is True

    def test_check_id_uniqueness_duplicate(self):
        """ID一意性チェック（重複あり）"""
        loader = DataLoader()
        data = [
            {"id": "test:id1", "title": "Test 1"},
            {"id": "test:id2", "title": "Test 2"},
            {"id": "test:id1", "title": "Test 1 Duplicate"},
        ]

        with pytest.raises(AnalyzerError, match="ID重複が検出されました"):
            loader.check_id_uniqueness(data)


class TestComparisonEngine:
    """ComparisonEngineクラスのユニットテスト"""

    def test_detect_added_items(self):
        """新規追加の検出"""
        engine = ComparisonEngine()

        previous_ids = {"test:id1", "test:id2"}
        current_dict = {
            "test:id1": {"id": "test:id1", "title": "Test 1"},
            "test:id2": {"id": "test:id2", "title": "Test 2"},
            "test:id3": {"id": "test:id3", "title": "Test 3"},
        }

        result = engine.detect_added(previous_ids, current_dict)

        assert len(result) == 1
        assert result[0]["id"] == "test:id3"

    def test_detect_removed_items(self):
        """削除の検出"""
        engine = ComparisonEngine()

        previous_dict = {
            "test:id1": {"id": "test:id1", "title": "Test 1"},
            "test:id2": {"id": "test:id2", "title": "Test 2"},
            "test:id3": {"id": "test:id3", "title": "Test 3"},
        }
        current_ids = {"test:id1", "test:id2"}

        result = engine.detect_removed(previous_dict, current_ids)

        assert len(result) == 1
        assert result[0]["id"] == "test:id3"

    def test_detect_changed_items(self):
        """内容変更の検出"""
        engine = ComparisonEngine(use_content_hash=False)

        previous_dict = {
            "test:id1": {
                "id": "test:id1",
                "title": "Test 1",
                "version": "1.0",
                "observed_at": "2026-01-28T10:00:00+09:00",
            }
        }
        current_dict = {
            "test:id1": {
                "id": "test:id1",
                "title": "Test 1",
                "version": "1.1",
                "observed_at": "2026-01-28T11:00:00+09:00",
            }
        }

        result = engine.detect_changed(previous_dict, current_dict)

        assert len(result) == 1
        assert result[0]["id"] == "test:id1"
        assert "changes" in result[0]
        assert len(result[0]["changes"]) == 1
        assert result[0]["changes"][0]["field"] == "version"

    def test_detect_changed_with_content_hash_same(self):
        """content_hash最適化（ハッシュ値同じ）"""
        engine = ComparisonEngine(use_content_hash=True)

        previous_dict = {
            "test:id1": {
                "id": "test:id1",
                "title": "Test 1",
                "content_hash": "abc123",
                "observed_at": "2026-01-28T10:00:00+09:00",
            }
        }
        current_dict = {
            "test:id1": {
                "id": "test:id1",
                "title": "Test 1",
                "content_hash": "abc123",
                "observed_at": "2026-01-28T11:00:00+09:00",
            }
        }

        result = engine.detect_changed(previous_dict, current_dict)

        # ハッシュ値が同じなので変更なし
        assert len(result) == 0

    def test_detect_changed_with_content_hash_different(self):
        """content_hash最適化（ハッシュ値異なる）"""
        engine = ComparisonEngine(use_content_hash=True)

        previous_dict = {
            "test:id1": {
                "id": "test:id1",
                "title": "Test 1",
                "version": "1.0",
                "content_hash": "abc123",
                "observed_at": "2026-01-28T10:00:00+09:00",
            }
        }
        current_dict = {
            "test:id1": {
                "id": "test:id1",
                "title": "Test 1",
                "version": "1.1",
                "content_hash": "def456",
                "observed_at": "2026-01-28T11:00:00+09:00",
            }
        }

        result = engine.detect_changed(previous_dict, current_dict)

        # ハッシュ値が異なるので詳細比較実行
        assert len(result) == 1
        assert result[0]["changes"][0]["field"] == "version"

    def test_compare_datasets_full(self):
        """データセット比較（統合）"""
        engine = ComparisonEngine(use_content_hash=False)

        previous_data = [
            {"id": "test:id1", "title": "Test 1", "version": "1.0"},
            {"id": "test:id2", "title": "Test 2", "version": "2.0"},
            {"id": "test:id3", "title": "Test 3", "version": "3.0"},
        ]
        current_data = [
            {"id": "test:id1", "title": "Test 1", "version": "1.1"},
            {"id": "test:id2", "title": "Test 2", "version": "2.0"},
            {"id": "test:id4", "title": "Test 4", "version": "4.0"},
        ]

        result = engine.compare_datasets(previous_data, current_data)

        assert result["summary"]["added_count"] == 1
        assert result["summary"]["removed_count"] == 1
        assert result["summary"]["changed_count"] == 1
        assert result["added"][0]["id"] == "test:id4"
        assert result["removed"][0]["id"] == "test:id3"
        assert result["changed"][0]["id"] == "test:id1"


class TestHistoryManager:
    """HistoryManagerクラスのユニットテスト"""

    def test_save_history_success(self, tmp_path):
        """履歴データの保存（成功）"""
        manager = HistoryManager(str(tmp_path), max_history_days=30)

        test_data = [
            {"id": "test:id1", "title": "Test 1"},
            {"id": "test:id2", "title": "Test 2"},
        ]

        result = manager.save_history("test-source", test_data)

        assert result is True

        # ファイルが作成されたことを確認
        history_files = list(tmp_path.glob("test-source_*.json"))
        assert len(history_files) == 1

        # 内容を確認
        with history_files[0].open("r", encoding="utf-8") as f:
            saved_data = json.load(f)
        assert len(saved_data) == 2
        assert saved_data[0]["id"] == "test:id1"

    def test_load_history_success(self, tmp_path):
        """履歴データの読み込み（成功）"""
        manager = HistoryManager(str(tmp_path), max_history_days=30)

        # 履歴データを作成
        test_data = [
            {"id": "test:id1", "title": "Test 1"},
            {"id": "test:id2", "title": "Test 2"},
        ]
        manager.save_history("test-source", test_data)

        # 読み込み
        result = manager.load_history("test-source")

        assert result is not None
        assert len(result) == 2
        assert result[0]["id"] == "test:id1"

    def test_load_history_not_found(self, tmp_path):
        """履歴データの読み込み（存在しない）"""
        manager = HistoryManager(str(tmp_path), max_history_days=30)

        result = manager.load_history("nonexistent-source")

        assert result is None

    def test_cleanup_old_history(self, tmp_path):
        """古い履歴の削除"""
        manager = HistoryManager(str(tmp_path), max_history_days=0)

        # 複数の履歴を作成
        test_data = [{"id": "test:id1", "title": "Test 1"}]

        manager.save_history("test-source", test_data)
        manager.save_history("test-source", test_data)

        # 最新のみ残る
        history_files = list(tmp_path.glob("test-source_*.json"))
        assert len(history_files) == 1


class TestDiffAnalyzer:
    """DiffAnalyzerクラスのユニットテスト"""

    def test_initialization(self, tmp_path):
        """初期化テスト"""
        settings = {
            "storage": {"history_directory": str(tmp_path)},
            "comparison": {"use_content_hash": True},
        }

        analyzer = DiffAnalyzer(settings)

        assert analyzer.settings == settings
        assert analyzer.data_loader is not None
        assert analyzer.comparison_engine is not None
        assert analyzer.history_manager is not None

    def test_analyze_changes_first_run(self, tmp_path):
        """初回実行の差分分析"""
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
            },
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id2",
                "type": "release",
                "title": "Test 2",
                "url": "https://example.com/2",
                "observed_at": "2026-01-28T10:00:00+09:00",
            },
        ]

        with test_file.open("w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 設定
        history_dir = tmp_path / "history"
        settings = {
            "storage": {"history_directory": str(history_dir)},
            "comparison": {"use_content_hash": False},
        }

        analyzer = DiffAnalyzer(settings)
        result = analyzer.analyze_changes("test-source", str(test_file))

        # 初回実行なので全て新規追加
        assert result["summary"]["added_count"] == 2
        assert result["summary"]["removed_count"] == 0
        assert result["summary"]["changed_count"] == 0

        # 履歴が保存されたことを確認
        history_files = list(history_dir.glob("test-source_*.json"))
        assert len(history_files) == 1

    def test_analyze_changes_with_history(self, tmp_path):
        """履歴ありの差分分析"""
        # 前回データを作成
        history_dir = tmp_path / "history"
        history_dir.mkdir()

        previous_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T10:00:00+09:00",
                "version": "1.0",
            }
        ]

        history_file = history_dir / "test-source_20260128_100000.json"
        with history_file.open("w", encoding="utf-8") as f:
            json.dump(previous_data, f)

        # 今回データを作成（バージョンが変更）
        test_file = tmp_path / "test.jsonl"
        current_data = [
            {
                "schema": "okina.item.v1",
                "source": "test",
                "id": "test:id1",
                "type": "release",
                "title": "Test 1",
                "url": "https://example.com/1",
                "observed_at": "2026-01-28T11:00:00+09:00",
                "version": "1.1",
            }
        ]

        with test_file.open("w", encoding="utf-8") as f:
            for item in current_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        # 設定
        settings = {
            "storage": {"history_directory": str(history_dir)},
            "comparison": {"use_content_hash": False},
        }

        analyzer = DiffAnalyzer(settings)
        result = analyzer.analyze_changes("test-source", str(test_file))

        # バージョン変更が検出される
        assert result["summary"]["added_count"] == 0
        assert result["summary"]["removed_count"] == 0
        assert result["summary"]["changed_count"] == 1
        assert result["changed"][0]["id"] == "test:id1"
