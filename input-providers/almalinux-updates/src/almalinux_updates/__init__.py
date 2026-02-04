"""
AlmaLinux Updates Provider for Okina

AlmaLinux（RHEL系）システムで利用可能なパッケージ更新を自動検知し、
Okinaプロジェクトの標準データ形式で出力するInput Provider。
"""

__version__ = "0.1.0"
__author__ = "kamonabe"

__all__ = [
    "ConfigManager",
    "DNFCommandRunner",
    "SystemAnalyzer",
    "DataNormalizer",
    "ErrorHandler",
]
