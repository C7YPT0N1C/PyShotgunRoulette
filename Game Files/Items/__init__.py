import os
import importlib

# Dynamically import all `*Item.py` files in this folder
modules = {}
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith("Item.py"):
        module_name = file[:-3]  # Remove '.py' extension
        module = importlib.import_module(f"Items.{module_name}")
        modules[module_name] = module

# Make imported modules accessible via `Items`
__all__ = list(modules.keys())