"""
pytest設定ファイル
テスト共通の設定とフィクスチャを定義
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock


@pytest.fixture
def temp_dir():
    """一時ディレクトリを作成するフィクスチャ"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_jsonl_data():
    """サンプルのJSONLデータ"""
    return [
        {
            "schema": "okina.item.v1",
            "source": "test-source",
            "id": "test:product:1.0.0:release",
            "type": "release",
            "title": "Test Product 1.0.0",
            "url": "https://example.com/1.0.0",
            "observed_at": "2025-12-22T10:00:00+09:00",
            "version": "1.0.0"
        },
        {
            "schema": "okina.item.v1", 
            "source": "test-source",
            "id": "test:product:1.1.0:release",
            "type": "release",
            "title": "Test Product 1.1.0",
            "url": "https://example.com/1.1.0",
            "observed_at": "2025-12-22T11:00:00+09:00",
            "version": "1.1.0"
        }
    ]


@pytest.fixture
def mock_settings():
    """モック設定オブジェクト"""
    return {
        "profile": {"usage": "dev"},
        "input": {
            "data_directory": "data/input",
            "file_pattern": "*.jsonl"
        },
        "storage": {
            "history_directory": "data/history",
            "max_history_days": 30
        },
        "notifications": {
            "slack": {
                "enabled": True,
                "webhook_url": "https://hooks.slack.com/test"
            }
        },
        "output": {
            "default_mode": "normal",
            "max_items_per_notification": 10
        },
        "logging": {
            "level": "INFO",
            "file": "log/okina.log"
        }
    }


@pytest.fixture
def mock_notification_manager():
    """モック通知マネージャー"""
    mock = Mock()
    mock.send_notification.return_value = True
    return mock