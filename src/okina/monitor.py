#!/usr/bin/env python3
"""
変化監視システム - 翁らしく静かに見守る

このモジュールはOkinaプロジェクトの一部として、
正規化データの監視、差分抽出と通知の統合制御を提供します。

Author: kamonabe
Created: 2026-01-28
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import glob

# プロジェクト内インポート
from okina.exceptions import OkinaError
from okina.analyzer import DiffAnalyzer, AnalyzerError
from okina.notification import NotificationManager, NotificationError

# ロガー設定
logger = logging.getLogger(__name__)


class MonitorError(OkinaError):
    """
    変化監視システム固有のエラー

    このクラスは変化監視システムの処理中に発生する
    特定のエラー状況を表現します。
    """

    pass


class ConfigManager:
    """
    設定管理クラス

    YAML設定ファイルの読み込み、検証、環境変数解決を行います。

    翁らしい設計原則:
    - シンプルな設定構造
    - 明確なエラーメッセージ
    - デフォルト値による柔軟性

    Example:
        >>> manager = ConfigManager()
        >>> config = manager.load_config("settings.yml")
        >>> assert "input" in config
    """

    def __init__(self) -> None:
        """ConfigManagerを初期化"""
        logger.debug("ConfigManager initialized")

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        設定ファイルを読み込む

        Args:
            config_path (str): 設定ファイルパス

        Returns:
            Dict[str, Any]: 設定辞書

        Raises:
            MonitorError: 設定ファイル読み込みエラー
        """
        try:
            path = Path(config_path)

            if not path.exists():
                raise MonitorError(f"設定ファイルが見つかりません: {config_path}")

            with path.open("r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            if not config:
                raise MonitorError(f"設定ファイルが空です: {config_path}")

            # 設定を検証
            self.validate_config(config)

            logger.info(f"設定ファイル読み込み完了: {config_path}")
            return config

        except yaml.YAMLError as e:
            raise MonitorError(f"設定ファイルの形式が不正です: {e}")
        except MonitorError:
            raise
        except Exception as e:
            raise MonitorError(f"設定ファイル読み込みエラー: {e}")

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        設定内容を検証

        Args:
            config (Dict[str, Any]): 設定辞書

        Returns:
            bool: 検証成功時True

        Raises:
            MonitorError: 設定検証エラー
        """
        # 必須セクションのチェック
        required_sections = ["input", "storage", "notifications"]

        for section in required_sections:
            if section not in config:
                raise MonitorError(f"必須設定セクション '{section}' が不足しています")

        # input設定の検証
        if "data_directory" not in config["input"]:
            raise MonitorError("input.data_directory が設定されていません")

        # storage設定の検証
        if "history_directory" not in config["storage"]:
            raise MonitorError("storage.history_directory が設定されていません")

        # notifications設定の検証
        if not config["notifications"]:
            logger.warning("通知設定が空です")

        logger.debug("設定検証完了")
        return True


class DataWatcher:
    """
    データ監視クラス

    正規化データファイルの監視と検出を行います。

    翁らしい設計原則:
    - 静かなファイル検索
    - 適切なエラーハンドリング
    - 明確なログ記録

    Example:
        >>> watcher = DataWatcher()
        >>> files = watcher.find_source_files("data/input", "*.jsonl")
        >>> assert isinstance(files, list)
    """

    def __init__(self) -> None:
        """DataWatcherを初期化"""
        logger.debug("DataWatcher initialized")

    def find_source_files(
        self, data_directory: str, file_pattern: str = "*.jsonl"
    ) -> List[str]:
        """
        ソースファイルを検出

        Args:
            data_directory (str): データディレクトリ
            file_pattern (str): ファイルパターン

        Returns:
            List[str]: ソースファイルパスのリスト

        Raises:
            MonitorError: ディレクトリアクセスエラー
        """
        try:
            data_path = Path(data_directory)

            if not data_path.exists():
                raise MonitorError(f"データディレクトリが見つかりません: {data_directory}")

            if not data_path.is_dir():
                raise MonitorError(f"データディレクトリではありません: {data_directory}")

            # ファイルパターンで検索
            pattern = str(data_path / file_pattern)
            files = glob.glob(pattern)

            logger.info(f"ソースファイル検出: {len(files)}件 ({data_directory})")
            return sorted(files)

        except MonitorError:
            raise
        except Exception as e:
            raise MonitorError(f"ファイル検索エラー: {e}")

    def extract_source_name(self, file_path: str) -> str:
        """
        ファイルパスからソース名を抽出

        Args:
            file_path (str): ファイルパス

        Returns:
            str: ソース名

        Example:
            >>> watcher = DataWatcher()
            >>> name = watcher.extract_source_name("data/input/fortinet.jsonl")
            >>> assert name == "fortinet"
        """
        path = Path(file_path)
        # 拡張子を除いたファイル名をソース名とする
        source_name = path.stem
        return source_name


class ProcessController:
    """
    処理制御クラス

    差分抽出と通知の統合制御を行います。

    翁らしい設計原則:
    - 静かな処理制御
    - 適切な判断委譲
    - 確実なエラー報告

    Attributes:
        diff_analyzer (DiffAnalyzer): 差分抽出システム
        notification_manager (NotificationManager): 通知システム
    """

    def __init__(
        self,
        diff_analyzer: DiffAnalyzer,
        notification_manager: NotificationManager,
    ) -> None:
        """
        ProcessControllerを初期化

        Args:
            diff_analyzer (DiffAnalyzer): 差分抽出システム
            notification_manager (NotificationManager): 通知システム
        """
        self.diff_analyzer = diff_analyzer
        self.notification_manager = notification_manager
        logger.debug("ProcessController initialized")

    def process_source(
        self, source_name: str, file_path: str
    ) -> Dict[str, Any]:
        """
        単一ソースを処理

        Args:
            source_name (str): ソース名
            file_path (str): ファイルパス

        Returns:
            Dict[str, Any]: 処理結果
        """
        start_time = time.time()
        result = {
            "source_name": source_name,
            "file_path": file_path,
            "success": False,
            "notification_sent": False,
            "processing_time": 0.0,
        }

        try:
            logger.info(f"ソース処理開始: {source_name}")

            # 差分抽出を実行
            diff_result = self.diff_analyzer.analyze_changes(source_name, file_path)
            result["diff_result"] = diff_result

            # 変化があれば通知
            summary = diff_result["summary"]
            has_changes = (
                summary["added_count"] > 0
                or summary["removed_count"] > 0
                or summary["changed_count"] > 0
            )

            if has_changes:
                changes = {
                    "added": summary["added_count"],
                    "changed": summary["changed_count"],
                    "removed": summary["removed_count"],
                }

                notification_success = self.notification_manager.send_change_notification(
                    changes, source_name
                )

                result["notification_sent"] = notification_success

                if notification_success:
                    logger.info(f"変化通知送信完了: {source_name}")
                else:
                    logger.warning(f"変化通知送信失敗: {source_name}")
            else:
                logger.debug(f"変化なし: {source_name}")

            result["success"] = True

        except AnalyzerError as e:
            logger.error(f"差分抽出エラー ({source_name}): {e}")
            result["error"] = str(e)

            # 異常通知を送信
            self.notification_manager.send_error_notification(
                "差分抽出エラー", str(e), source_name
            )

        except Exception as e:
            logger.error(f"処理エラー ({source_name}): {e}")
            result["error"] = str(e)

            # 異常通知を送信
            self.notification_manager.send_error_notification(
                "システムエラー", str(e), source_name
            )

        finally:
            result["processing_time"] = time.time() - start_time
            logger.info(
                f"ソース処理完了: {source_name} "
                f"({result['processing_time']:.2f}秒)"
            )

        return result


class ErrorHandler:
    """
    エラー処理クラス

    エラー処理と異常通知を統合管理します。

    翁らしい設計原則:
    - 控えめなエラー報告
    - 継続性の重視
    - 適切なログ記録
    """

    def __init__(self, notification_manager: NotificationManager) -> None:
        """
        ErrorHandlerを初期化

        Args:
            notification_manager (NotificationManager): 通知システム
        """
        self.notification_manager = notification_manager
        logger.debug("ErrorHandler initialized")

    def handle_error(
        self,
        error_type: str,
        error_message: str,
        source: Optional[str] = None,
        should_abort: bool = False,
    ) -> None:
        """
        エラーを処理

        Args:
            error_type (str): エラー種別
            error_message (str): エラーメッセージ
            source (Optional[str]): エラーが発生したソース
            should_abort (bool): 処理を中断すべきか
        """
        # ログレベルを決定
        if should_abort:
            log_level = logging.CRITICAL
        else:
            log_level = logging.ERROR

        # ログに記録
        if source:
            logger.log(log_level, f"{error_type} ({source}): {error_message}")
        else:
            logger.log(log_level, f"{error_type}: {error_message}")

        # 異常通知を送信
        try:
            self.notification_manager.send_error_notification(
                error_type, error_message, source
            )
        except Exception as e:
            logger.warning(f"異常通知送信失敗: {e}")


class ChangeMonitor:
    """
    変化監視システム統合管理クラス

    このクラスは正規化データの監視、差分抽出と通知の統合制御を
    統合管理する機能を提供します。

    翁らしい設計原則:
    - 静かに見守る
    - 前と違えば知らせる
    - 判断は人に委ねる

    Attributes:
        config (Dict[str, Any]): 設定辞書
        config_manager (ConfigManager): 設定管理
        data_watcher (DataWatcher): データ監視
        diff_analyzer (DiffAnalyzer): 差分抽出
        notification_manager (NotificationManager): 通知管理
        process_controller (ProcessController): 処理制御
        error_handler (ErrorHandler): エラー処理

    Example:
        >>> monitor = ChangeMonitor("settings.yml")
        >>> success = monitor.run()
        >>> assert isinstance(success, bool)
    """

    def __init__(self, config_path: str = "settings.yml") -> None:
        """
        ChangeMonitorを初期化

        Args:
            config_path (str): 設定ファイルパス
        """
        # 設定を読み込む
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config(config_path)

        # コンポーネントを初期化
        self.data_watcher = DataWatcher()

        # 差分抽出システムを初期化
        analyzer_settings = {
            "storage": self.config.get("storage", {}),
            "comparison": self.config.get("comparison", {}),
        }
        self.diff_analyzer = DiffAnalyzer(analyzer_settings)

        # 通知システムを初期化
        notification_config = self.config.get("notifications", {})
        self.notification_manager = NotificationManager(notification_config)

        # 処理制御を初期化
        self.process_controller = ProcessController(
            self.diff_analyzer, self.notification_manager
        )

        # エラー処理を初期化
        self.error_handler = ErrorHandler(self.notification_manager)

        logger.info("ChangeMonitor initialized")

    def run(self) -> bool:
        """
        変化監視のメイン処理

        Returns:
            bool: 処理成功時True

        Example:
            >>> monitor = ChangeMonitor("settings.yml")
            >>> success = monitor.run()
        """
        try:
            logger.info("変化監視を開始します")

            # 変化監視を実行
            result = self.watch_changes()

            # 結果をログに記録
            logger.info(
                f"変化監視完了: "
                f"処理{result['sources_processed']}件, "
                f"変化{result['sources_with_changes']}件, "
                f"時間{result['processing_time']:.2f}秒"
            )

            return result["success"]

        except MonitorError as e:
            logger.critical(f"変化監視エラー: {e}")
            self.error_handler.handle_error(
                "変化監視エラー", str(e), should_abort=True
            )
            return False

        except Exception as e:
            logger.critical(f"予期しないエラー: {e}")
            self.error_handler.handle_error(
                "システムエラー", str(e), should_abort=True
            )
            return False

    def watch_changes(self) -> Dict[str, Any]:
        """
        変化監視の実行

        Returns:
            Dict[str, Any]: 監視結果サマリー
        """
        start_time = time.time()

        result = {
            "success": True,
            "sources_processed": 0,
            "sources_with_changes": 0,
            "total_changes": {"added": 0, "removed": 0, "changed": 0},
            "errors": [],
            "processing_time": 0.0,
        }

        try:
            # ソースファイルを検出
            data_directory = self.config["input"]["data_directory"]
            file_pattern = self.config["input"].get("file_pattern", "*.jsonl")

            source_files = self.data_watcher.find_source_files(
                data_directory, file_pattern
            )

            if not source_files:
                logger.warning("処理対象のソースファイルが見つかりません")
                self.error_handler.handle_error(
                    "データなし異常",
                    f"ディレクトリ '{data_directory}' にファイルが見つかりません",
                )
                result["success"] = False
                return result

            # 各ソースを処理
            for file_path in source_files:
                source_name = self.data_watcher.extract_source_name(file_path)

                source_result = self.process_controller.process_source(
                    source_name, file_path
                )

                result["sources_processed"] += 1

                if source_result["success"]:
                    # 変化があったかチェック
                    if "diff_result" in source_result:
                        summary = source_result["diff_result"]["summary"]
                        has_changes = (
                            summary["added_count"] > 0
                            or summary["removed_count"] > 0
                            or summary["changed_count"] > 0
                        )

                        if has_changes:
                            result["sources_with_changes"] += 1
                            result["total_changes"]["added"] += summary["added_count"]
                            result["total_changes"]["removed"] += summary[
                                "removed_count"
                            ]
                            result["total_changes"]["changed"] += summary[
                                "changed_count"
                            ]
                else:
                    result["errors"].append(
                        {
                            "source": source_name,
                            "error": source_result.get("error", "Unknown error"),
                        }
                    )

        except MonitorError as e:
            logger.error(f"変化監視処理エラー: {e}")
            result["success"] = False
            result["errors"].append({"error": str(e)})

        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            result["success"] = False
            result["errors"].append({"error": str(e)})

        finally:
            result["processing_time"] = time.time() - start_time

        return result


# モジュールレベルの定数
DEFAULT_CONFIG_PATH = "settings.yml"
DEFAULT_FILE_PATTERN = "*.jsonl"


if __name__ == "__main__":
    # モジュール単体テスト用のコード
    import doctest

    # doctestを実行
    doctest.testmod(verbose=True)

    # 簡単な動作確認
    try:
        print("ChangeMonitor module loaded successfully")
    except Exception as e:
        print(f"Test failed: {e}")
