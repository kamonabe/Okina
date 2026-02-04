"""
ConfigManager - YAML設定ファイルの読み込みと管理

YAML設定ファイルを読み込み、デフォルト値を提供する。
設定ファイルが存在しない場合や無効な場合でも、適切なデフォルト値で動作を継続する。
"""
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml


class ConfigError(Exception):
    """設定ファイル関連のエラー"""
    pass


class ConfigManager:
    """YAML設定ファイルの読み込みと管理
    
    設定ファイルが存在しない場合はデフォルト値を使用。
    無効な設定値の場合は適切にエラー処理を行う。
    """
    
    # デフォルト設定値
    DEFAULT_CONFIG = {
        "dnf": {
            "timeout": 300,
            "network_timeout": 60,
        },
        "repositories": {
            "include": [],
            "exclude": [],
        },
        "update_types": ["security", "bugfix", "enhancement"],
        "severity": {
            "threshold": "low",
        },
        "execution": {
            "dry_run": False,
            "lock_file": "/tmp/almalinux-updates-provider.lock",
        },
        "logging": {
            "error_log": "error.log",
            "level": "INFO",
        },
    }
    
    def __init__(self, config_path: str = "config.yml") -> None:
        """ConfigManagerを初期化
        
        Args:
            config_path: 設定ファイルのパス（デフォルト: config.yml）
            
        Raises:
            ConfigError: 設定ファイルの構文エラー
        """
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """設定ファイルを読み込む
        
        設定ファイルが存在しない場合はデフォルト値を使用。
        """
        if not self.config_path.exists():
            # 設定ファイルが存在しない場合はデフォルト値を使用
            self._config = self.DEFAULT_CONFIG.copy()
            return
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded_config = yaml.safe_load(f)
                
            if loaded_config is None:
                # 空のファイルの場合
                self._config = self.DEFAULT_CONFIG.copy()
                return
            
            # デフォルト値とマージ
            self._config = self._merge_config(self.DEFAULT_CONFIG, loaded_config)
            
        except yaml.YAMLError as e:
            raise ConfigError(f"設定ファイルの構文エラー: {e}")
        except Exception as e:
            raise ConfigError(f"設定ファイルの読み込みエラー: {e}")
    
    def _merge_config(
        self, default: Dict[str, Any], loaded: Dict[str, Any]
    ) -> Dict[str, Any]:
        """デフォルト設定と読み込んだ設定をマージ
        
        Args:
            default: デフォルト設定
            loaded: 読み込んだ設定
            
        Returns:
            マージされた設定
        """
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # ネストされた辞書の場合は再帰的にマージ
                result[key] = self._merge_config(result[key], value)
            else:
                # それ以外は上書き
                result[key] = value
        
        return result

    
    def get_timeout(self) -> int:
        """dnfコマンドのタイムアウト値を取得
        
        Returns:
            タイムアウト値（秒）
        """
        return self._config["dnf"]["timeout"]
    
    def get_network_timeout(self) -> int:
        """ネットワークタイムアウト値を取得
        
        Returns:
            ネットワークタイムアウト値（秒）
        """
        return self._config["dnf"]["network_timeout"]
    
    def get_repositories(self) -> Dict[str, List[str]]:
        """監視対象リポジトリ設定を取得
        
        Returns:
            リポジトリ設定（include, exclude）
        """
        return self._config["repositories"]
    
    def get_update_types(self) -> List[str]:
        """監視対象更新タイプを取得
        
        Returns:
            更新タイプリスト（security, bugfix, enhancement）
        """
        return self._config["update_types"]
    
    def get_severity_threshold(self) -> str:
        """最小重要度レベルを取得
        
        Returns:
            重要度レベル（low, moderate, important, critical）
        """
        return self._config["severity"]["threshold"]
    
    def is_dry_run(self) -> bool:
        """ドライランモードかどうかを判定
        
        Returns:
            ドライランモードの場合True
        """
        return self._config["execution"]["dry_run"]
    
    def get_lock_file(self) -> str:
        """ロックファイルのパスを取得
        
        Returns:
            ロックファイルのパス
        """
        return self._config["execution"]["lock_file"]
    
    def get_error_log(self) -> str:
        """エラーログファイルのパスを取得
        
        Returns:
            エラーログファイルのパス
        """
        return self._config["logging"]["error_log"]
    
    def get_log_level(self) -> str:
        """ログレベルを取得
        
        Returns:
            ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        """
        return self._config["logging"]["level"]
