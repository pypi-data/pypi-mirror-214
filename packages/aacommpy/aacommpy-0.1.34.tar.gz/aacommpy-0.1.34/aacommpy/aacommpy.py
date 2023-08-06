import clr
import os
from aacommpy.category import categories

dll_path = os.path.join(os.path.dirname(__file__), 'AAComm.dll')

if os.path.isfile(dll_path):
    clr.AddReference(dll_path)
    for category in categories:
        if category["enable"]:
            exec(f"from {category['from']} import {category['name']}")

    __all__ = [category["name"] for category in categories if category["enable"]]
