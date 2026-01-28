#!/usr/bin/env python3
"""
差分抽出システム - 確実で信頼性の高い変化検知

このモジュールはOkinaプロジェクトの一部として、
正規化データの差分抽出、履歴管理、変化検知を提供します。

Author: kamonabe
Created: 2026-01-28
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime

# プロジェクト内インポート
from okina.exceptions import OkinaError

# ロガー設定
logger = logging.getLogger(__name__)


class AnalyzerError(OkinaError):
    """
    差分抽出システム固有のエラー

    このクラスは差分抽出システムの処理中に発生する
    特定のエラー状況を表現します。
    """

    pass


class DataLoader:
    """
    正規化データ読み込みクラス

    JSON Lines形式の正規化データを読み込み、検証する機能を提供します。

    翁らしい設計原則:
    - 静かなエラーハンドリング
    - 部分的な失敗でも可能な範囲で処理継続
    - 適切なログ記録

    Example:
        >>> loader = DataLoader()
        >>> data = loader.load_jsonl("data/input/fortinet.jsonl")
        >>> assert isinstance(data, list)
    """

    def __init__(self) -> None:
        """DataLoaderを初期化"""
        logger.debug("DataLoader initialized")

    def load_jsonl(self, file_path: str) -> List[Dict[str, Any]]:
        """
        JSON Lines形式ファイルを読み込む

        Args:
            file_path (str): 読み込むファイルパス

        Returns:
            List[Dict[str, Any]]: 正規化データのリスト

        Raises:
            AnalyzerError: ファイル読み込みエラー
        """
        try:
            path = Path(file_path)

            if not path.exists():
                raise AnalyzerError(f"データファイルが見つかりません: {file_path}")

            data = []
            line_number = 0

            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line_number += 1
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        item = json.loads(line)
                        self._validate_item(item, line_number)
                        data.append(item)
                    except json.JSONDecodeError as e:
                        logger.warning(
                            f"JSON解析エラー (行{line_number}): {e} - スキップします"
                        )
                        continue
                    except ValueError as e:
                        logger.warning(f"データ検証エラー (行{line_number}): {e} - スキップします")
                        continue

            logger.info(f"データ読み込み完了: {len(data)}件 ({file_path})")
            return data

        except AnalyzerError:
            raise
        except Exception as e:
            raise AnalyzerError(f"データ読み込みエラー: {e}")

    def _validate_item(self, item: Dict[str, Any], line_number: int) -> None:
        """
        アイテムの必須フィールドを検証

        Args:
            item (Dict[str, Any]): 検証するアイテム
            line_number (int): 行番号

        Raises:
            ValueError: 必須フィールドが不足している場合
        """
        required_fields = ["schema", "source", "id", "type", "title", "url", "observed_at"]

        for field in required_fields:
            if field not in item:
                raise ValueError(f"必須フィールド '{field}' が不足しています")

    def check_id_uniqueness(self, data: List[Dict[str, Any]]) -> bool:
        """
        ID一意性をチェック

        Args:
            data (List[Dict[str, Any]]): チェックするデータ

        Returns:
            bool: 一意性が保たれている場合True

        Raises:
            AnalyzerError: ID重複が検出された場合
        """
        ids = [item.get("id") for item in data]
        unique_ids = set(ids)

        if len(ids) != len(unique_ids):
            # 重複IDを特定
            seen = set()
            duplicates = set()
            for id_value in ids:
                if id_value in seen:
                    duplicates.add(id_value)
                seen.add(id_value)

            raise AnalyzerError(f"ID重複が検出されました: {duplicates}")

        return True


class ComparisonEngine:
    """
    データ比較エンジンクラス

    IDベース比較と内容変更検出を行う機能を提供します。

    アルゴリズム:
    - IDベース比較: O(n + m) の時間計算量
    - content_hash最適化: ハッシュ値が同じ場合は詳細比較スキップ
    - フィールドレベル比較: 変更されたフィールドを特定

    Example:
        >>> engine = ComparisonEngine()
        >>> previous = [{"id": "id1", "title": "v1.0"}]
        >>> current = [{"id": "id1", "title": "v1.1"}]
        >>> result = engine.compare_datasets(previous, current)
        >>> assert result["changed_count"] == 1
    """

    def __init__(self, use_content_hash: bool = True) -> None:
        """
        ComparisonEngineを初期化

        Args:
            use_content_hash (bool): content_hash最適化を使用するか
        """
        self.use_content_hash = use_content_hash
        logger.debug(f"ComparisonEngine initialized (use_content_hash={use_content_hash})")

    def compare_datasets(
        self, previous_data: List[Dict[str, Any]], current_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        データセット比較のメイン処理

        Args:
            previous_data (List[Dict[str, Any]]): 前回データ
            current_data (List[Dict[str, Any]]): 今回データ

        Returns:
            Dict[str, Any]: 比較結果
                {
                    "added": [...],
                    "removed": [...],
                    "changed": [...],
                    "summary": {...}
                }
        """
        # IDセットを作成（高速比較用）
        previous_ids = {item["id"] for item in previous_data}
        current_ids = {item["id"] for item in current_data}

        # ID辞書を作成（詳細比較用）
        previous_dict = {item["id"]: item for item in previous_data}
        current_dict = {item["id"]: item for item in current_data}

        # 新規追加を検出
        added = self.detect_added(previous_ids, current_dict)

        # 削除を検出
        removed = self.detect_removed(previous_dict, current_ids)

        # 内容変更を検出
        changed = self.detect_changed(previous_dict, current_dict)

        # サマリーを作成
        summary = {
            "total_previous": len(previous_data),
            "total_current": len(current_data),
            "added_count": len(added),
            "removed_count": len(removed),
            "changed_count": len(changed),
        }

        logger.info(
            f"比較完了: 追加{summary['added_count']}件, "
            f"削除{summary['removed_count']}件, 変更{summary['changed_count']}件"
        )

        return {
            "added": added,
            "removed": removed,
            "changed": changed,
            "summary": summary,
        }

    def detect_added(
        self, previous_ids: Set[str], current_dict: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        新規追加を検出

        Args:
            previous_ids (Set[str]): 前回IDセット
            current_dict (Dict[str, Dict[str, Any]]): 今回データ辞書

        Returns:
            List[Dict[str, Any]]: 新規追加アイテム
        """
        added = []

        for id_value, item in current_dict.items():
            if id_value not in previous_ids:
                added.append(item)

        return added

    def detect_removed(
        self, previous_dict: Dict[str, Dict[str, Any]], current_ids: Set[str]
    ) -> List[Dict[str, Any]]:
        """
        削除を検出

        Args:
            previous_dict (Dict[str, Dict[str, Any]]): 前回データ辞書
            current_ids (Set[str]): 今回IDセット

        Returns:
            List[Dict[str, Any]]: 削除アイテム
        """
        removed = []

        for id_value, item in previous_dict.items():
            if id_value not in current_ids:
                removed.append(item)

        return removed

    def detect_changed(
        self,
        previous_dict: Dict[str, Dict[str, Any]],
        current_dict: Dict[str, Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        内容変更を検出

        Args:
            previous_dict (Dict[str, Dict[str, Any]]): 前回データ辞書
            current_dict (Dict[str, Dict[str, Any]]): 今回データ辞書

        Returns:
            List[Dict[str, Any]]: 変更アイテム（変更詳細付き）
        """
        changed = []

        # 共通IDについて内容変更をチェック
        common_ids = set(previous_dict.keys()) & set(current_dict.keys())

        for id_value in common_ids:
            prev_item = previous_dict[id_value]
            curr_item = current_dict[id_value]

            # content_hash最適化
            if self.use_content_hash:
                prev_hash = prev_item.get("content_hash")
                curr_hash = curr_item.get("content_hash")

                if prev_hash and curr_hash and prev_hash == curr_hash:
                    # ハッシュ値が同じ場合は変更なし
                    continue

            # フィールドレベルの詳細比較
            changes = self._compare_items(prev_item, curr_item)

            if changes:
                changed_item = curr_item.copy()
                changed_item["changes"] = changes
                changed.append(changed_item)

        return changed

    def _compare_items(
        self, prev_item: Dict[str, Any], curr_item: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        アイテムのフィールドレベル比較

        Args:
            prev_item (Dict[str, Any]): 前回アイテム
            curr_item (Dict[str, Any]): 今回アイテム

        Returns:
            List[Dict[str, Any]]: 変更詳細のリスト
        """
        changes = []

        # 比較対象外フィールド
        excluded_fields = {"observed_at", "content_hash"}

        # 全フィールドを比較
        all_fields = set(prev_item.keys()) | set(curr_item.keys())

        for field in all_fields:
            if field in excluded_fields:
                continue

            prev_value = prev_item.get(field)
            curr_value = curr_item.get(field)

            if prev_value != curr_value:
                change_detail = {
                    "field": field,
                    "old_value": prev_value,
                    "new_value": curr_value,
                    "description": f"{field}: {prev_value} → {curr_value}",
                }
                changes.append(change_detail)

        return changes


class HistoryManager:
    """
    履歴データ管理クラス

    前回データの保存と読み込みを管理する機能を提供します。

    翁らしい設計原則:
    - 正常終了時のみ履歴を更新
    - エラー時は前回データを保持
    - 古い履歴の自動削除

    Example:
        >>> manager = HistoryManager("data/history")
        >>> data = [{"id": "id1", "title": "test"}]
        >>> success = manager.save_history("fortinet", data)
        >>> assert success
    """

    def __init__(self, history_directory: str, max_history_days: int = 30) -> None:
        """
        HistoryManagerを初期化

        Args:
            history_directory (str): 履歴保存ディレクトリ
            max_history_days (int): 履歴保持日数
        """
        self.history_directory = Path(history_directory)
        self.max_history_days = max_history_days

        # ディレクトリを作成
        self.history_directory.mkdir(parents=True, exist_ok=True)

        logger.debug(f"HistoryManager initialized (dir={history_directory})")

    def load_history(self, source: str) -> Optional[List[Dict[str, Any]]]:
        """
        前回データを読み込む

        Args:
            source (str): データソース名

        Returns:
            Optional[List[Dict[str, Any]]]: 前回データ、存在しない場合None
        """
        try:
            # 最新の履歴ファイルを検索
            history_files = list(self.history_directory.glob(f"{source}_*.json"))

            if not history_files:
                logger.info(f"履歴データが見つかりません: {source} (初回実行)")
                return None

            # 最新ファイルを取得
            latest_file = max(history_files, key=lambda p: p.stat().st_mtime)

            with latest_file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            logger.info(f"履歴データ読み込み: {len(data)}件 ({latest_file.name})")
            return data

        except Exception as e:
            logger.warning(f"履歴データ読み込みエラー: {e} - 初回実行として処理します")
            return None

    def save_history(self, source: str, data: List[Dict[str, Any]]) -> bool:
        """
        履歴データを保存

        Args:
            source (str): データソース名
            data (List[Dict[str, Any]]): 保存するデータ

        Returns:
            bool: 保存成功時True
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{source}_{timestamp}.json"
            filepath = self.history_directory / filename

            with filepath.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"履歴データ保存: {len(data)}件 ({filename})")

            # 古い履歴を削除
            self._cleanup_old_history(source)

            return True

        except Exception as e:
            logger.error(f"履歴データ保存エラー: {e}")
            return False

    def _cleanup_old_history(self, source: str) -> None:
        """
        古い履歴ファイルを削除

        Args:
            source (str): データソース名
        """
        try:
            history_files = list(self.history_directory.glob(f"{source}_*.json"))

            # 日付でソート（新しい順）
            history_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            # 保持日数を超えるファイルを削除
            cutoff_time = datetime.now().timestamp() - (self.max_history_days * 86400)

            deleted_count = 0
            for filepath in history_files[1:]:  # 最新は残す
                if filepath.stat().st_mtime < cutoff_time:
                    filepath.unlink()
                    deleted_count += 1

            if deleted_count > 0:
                logger.debug(f"古い履歴を削除: {deleted_count}件")

        except Exception as e:
            logger.warning(f"履歴クリーンアップエラー: {e}")


class DiffAnalyzer:
    """
    差分抽出システム統合管理クラス

    このクラスは正規化データの差分抽出、履歴管理、変化検知を
    統合管理する機能を提供します。

    翁らしい設計原則:
    - 確実で信頼性の高い変化検知
    - 静かなエラーハンドリング
    - 適切なログ記録

    Attributes:
        settings (Dict[str, Any]): 差分抽出設定
        data_loader (DataLoader): データ読み込み
        comparison_engine (ComparisonEngine): 比較エンジン
        history_manager (HistoryManager): 履歴管理

    Example:
        >>> settings = {
        ...     "storage": {"history_directory": "data/history"},
        ...     "comparison": {"use_content_hash": True}
        ... }
        >>> analyzer = DiffAnalyzer(settings)
        >>> result = analyzer.analyze_changes("fortinet", "data/input/fortinet.jsonl")
        >>> assert "summary" in result
    """

    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        """
        DiffAnalyzerを初期化

        Args:
            settings (Optional[Dict[str, Any]]): 差分抽出設定
        """
        self.settings = settings or {}

        # コンポーネントを初期化
        self.data_loader = DataLoader()

        use_content_hash = self.settings.get("comparison", {}).get("use_content_hash", True)
        self.comparison_engine = ComparisonEngine(use_content_hash=use_content_hash)

        history_dir = self.settings.get("storage", {}).get("history_directory", "data/history")
        max_history_days = self.settings.get("storage", {}).get("max_history_days", 30)
        self.history_manager = HistoryManager(history_dir, max_history_days)

        logger.info("DiffAnalyzer initialized")

    def analyze_changes(self, source: str, input_file_path: str) -> Dict[str, Any]:
        """
        変化分析のメイン処理

        Args:
            source (str): データソース名
            input_file_path (str): 正規化データファイルパス

        Returns:
            Dict[str, Any]: 差分結果
                {
                    "added": [...],
                    "removed": [...],
                    "changed": [...],
                    "summary": {...}
                }

        Raises:
            AnalyzerError: 分析エラー
        """
        try:
            logger.info(f"差分分析開始: {source}")

            # 今回データを読み込む
            current_data = self.data_loader.load_jsonl(input_file_path)

            # ID一意性をチェック
            self.data_loader.check_id_uniqueness(current_data)

            # 前回データを読み込む
            previous_data = self.history_manager.load_history(source)

            if previous_data is None:
                # 初回実行: 全データを新規追加として扱う
                logger.info("初回実行: 全データを新規追加として処理します")
                result = {
                    "added": current_data,
                    "removed": [],
                    "changed": [],
                    "summary": {
                        "total_previous": 0,
                        "total_current": len(current_data),
                        "added_count": len(current_data),
                        "removed_count": 0,
                        "changed_count": 0,
                    },
                }
            else:
                # 差分を抽出
                result = self.comparison_engine.compare_datasets(previous_data, current_data)

            # 正常終了時のみ履歴を保存
            self.history_manager.save_history(source, current_data)

            logger.info(f"差分分析完了: {source}")
            return result

        except AnalyzerError:
            raise
        except Exception as e:
            raise AnalyzerError(f"差分分析エラー: {e}")


# モジュールレベルの定数
DEFAULT_HISTORY_DAYS = 30
MAX_ITEMS_LIMIT = 10000


if __name__ == "__main__":
    # モジュール単体テスト用のコード
    import doctest

    # doctestを実行
    doctest.testmod(verbose=True)

    # 簡単な動作確認
    try:
        settings = {
            "storage": {"history_directory": "data/history"},
            "comparison": {"use_content_hash": True},
        }
        analyzer = DiffAnalyzer(settings)
        print("DiffAnalyzer initialized successfully")
    except Exception as e:
        print(f"Test failed: {e}")
