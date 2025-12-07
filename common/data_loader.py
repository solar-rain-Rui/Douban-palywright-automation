import yaml
import os


def load_yaml(path):
    """
    读取 YAML 并返回 dict
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"YAML 文件不存在：{path}")

    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)
