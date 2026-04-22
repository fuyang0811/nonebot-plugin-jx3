"""自动导入所有命令子模块"""
from pathlib import Path
from importlib import import_module

_dir = Path(__file__).parent
for f in _dir.glob("*.py"):
    if f.name != "__init__.py":
        import_module(f".{f.stem}", package=__name__)
