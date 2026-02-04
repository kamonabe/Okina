"""
ConfigManager Unit Tests

ConfigManagerのユニットテスト。
設定ファイルの読み込み、デフォルト値の使用、エラー処理を検証。
"""
import pytest
import tempfile
from pathlib import Path
from almalinux_updates.config_manager import ConfigManager, ConfigError


class TestConfigManager:
    """ConfigManagerのユニットテスト"""
    
    def test_default_config_when_file_not_exists(self):
        """設定ファイルが存在しない場合、デフォルト値が使用される"""
        config = ConfigManager("nonexistent.yml")
        
        assert config.get_timeout() == 300
        assert config.get_network_timeout() == 60
        assert config.get_update_types() == ["security", "bugfix", "enhancement"]
        assert config.get_severity_threshold() == "low"
        assert config.is_dry_run() is False
        assert config.get_lock_file() == "/tmp/almalinux-updates-provider.lock"
        assert config.get_error_log() == "error.log"
        assert config.get_log_level() == "INFO"
    
    def test_load_valid_config_file(self):
        """正常な設定ファイルが正しく読み込まれる"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("""
dnf:
  timeout: 600
  network_timeout: 120
update_types:
  - security
severity:
  threshold: "important"
execution:
  dry_run: true
logging:
  level: "DEBUG"
""")
            config_path = f.name
        
        try:
            config = ConfigManager(config_path)
            
            assert config.get_timeout() == 600
            assert config.get_network_timeout() == 120
            assert config.get_update_types() == ["security"]
            assert config.get_severity_threshold() == "important"
            assert config.is_dry_run() is True
            assert config.get_log_level() == "DEBUG"
        finally:
            Path(config_path).unlink()
    
    def test_partial_config_uses_defaults(self):
        """部分的な設定ファイルの場合、未設定項目はデフォルト値が使用される"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("""
dnf:
  timeout: 450
""")
            config_path = f.name
        
        try:
            config = ConfigManager(config_path)
            
            # 設定された値
            assert config.get_timeout() == 450
            # デフォルト値
            assert config.get_network_timeout() == 60
            assert config.get_update_types() == ["security", "bugfix", "enhancement"]
        finally:
            Path(config_path).unlink()
    
    def test_empty_config_file_uses_defaults(self):
        """空の設定ファイルの場合、全てデフォルト値が使用される"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("")
            config_path = f.name
        
        try:
            config = ConfigManager(config_path)
            
            assert config.get_timeout() == 300
            assert config.get_network_timeout() == 60
        finally:
            Path(config_path).unlink()
    
    def test_invalid_yaml_raises_config_error(self):
        """無効なYAML構文の場合、ConfigErrorが発生する"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("""
invalid: yaml: syntax:
  - broken
    indentation
""")
            config_path = f.name
        
        try:
            with pytest.raises(ConfigError) as exc_info:
                ConfigManager(config_path)
            
            assert "構文エラー" in str(exc_info.value)
        finally:
            Path(config_path).unlink()
    
    def test_get_repositories(self):
        """リポジトリ設定が正しく取得される"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("""
repositories:
  include:
    - baseos
    - appstream
  exclude:
    - extras
""")
            config_path = f.name
        
        try:
            config = ConfigManager(config_path)
            repos = config.get_repositories()
            
            assert repos["include"] == ["baseos", "appstream"]
            assert repos["exclude"] == ["extras"]
        finally:
            Path(config_path).unlink()
    
    def test_nested_config_merge(self):
        """ネストされた設定が正しくマージされる"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("""
dnf:
  timeout: 500
logging:
  error_log: "custom.log"
""")
            config_path = f.name
        
        try:
            config = ConfigManager(config_path)
            
            # 設定された値
            assert config.get_timeout() == 500
            assert config.get_error_log() == "custom.log"
            # デフォルト値（同じネスト内）
            assert config.get_network_timeout() == 60
            assert config.get_log_level() == "INFO"
        finally:
            Path(config_path).unlink()

