"""
Okina（翁） - ファームウェア・ソフトウェア更新の変化検知ツール

静かに見守り、前と違えば知らせ、判断は人に委ねる
縁側に座って世界を見ている翁のような存在
"""

__version__ = "0.1.0"
__author__ = "kamonabe"
__email__ = "kamonabe1927@gmail.com"

# 実装済みのモジュールのみインポート
from .notification import NotificationManager, MessageFormatter
from .exceptions import OkinaError, NotificationError

__all__ = [
    "NotificationManager",
    "MessageFormatter",
    "OkinaError",
    "NotificationError",
]
