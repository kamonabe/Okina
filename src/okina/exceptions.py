#!/usr/bin/env python3
"""
Okina例外クラス

このモジュールはOkinaプロジェクト固有の例外クラスを定義します。
翁らしい静かで継続性を重視したエラーハンドリングを提供します。

Author: kamonabe
Created: 2026-01-06
"""


class OkinaError(Exception):
    """
    Okina基底例外クラス

    Okinaプロジェクトの全ての例外の基底クラスです。
    翁らしい静かで継続性を重視したエラーハンドリングの原則に従います。

    翁らしいエラーハンドリング原則:
    - 完璧を求めず、継続性を重視
    - 過度に警告せず、静かに記録
    - 部分的な失敗でも可能な限り処理を継続
    """

    pass


class ChangeDetectionError(OkinaError):
    """変化検知システムのエラー"""

    pass


class DiffAnalysisError(OkinaError):
    """差分抽出システムのエラー"""

    pass


class NotificationError(OkinaError):
    """通知システムのエラー"""

    pass


class ConfigurationError(OkinaError):
    """設定関連のエラー"""

    pass


class DataProcessingError(OkinaError):
    """データ処理関連のエラー"""

    pass
