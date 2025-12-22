#!/usr/bin/env python3
"""
Okina メイン実行スクリプト
変化検知を実行する
"""

import sys
import os
from pathlib import Path

# src/okina をPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from okina.cli import main

if __name__ == "__main__":
    main()