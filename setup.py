"""
Okina（翁） - ファームウェア・ソフトウェア更新の変化検知ツール
セットアップスクリプト
"""

from setuptools import setup, find_packages
from pathlib import Path

# README.mdを読み込む
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# version.txtからバージョンを読み込む
version = (this_directory / "version.txt").read_text(encoding="utf-8").strip()

setup(
    name="okina",
    version=version,
    description="ファームウェア・ソフトウェア更新の変化検知ツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="kamonabe",
    author_email="kamonabe1927@gmail.com",
    url="https://github.com/kamonabe/Okina",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "PyYAML>=6.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "okina=okina.cli:main",
        ],
    },
    data_files=[
        ("config", ["config/settings.yml.sample"]),
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Monitoring",
        "Topic :: Software Development :: Version Control",
    ],
    python_requires=">=3.10",
    include_package_data=True,
)