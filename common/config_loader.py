from pathlib import Path

import yaml


def load_config():
    """读取项目根目录 config/config.yaml。"""
    config_path = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)
