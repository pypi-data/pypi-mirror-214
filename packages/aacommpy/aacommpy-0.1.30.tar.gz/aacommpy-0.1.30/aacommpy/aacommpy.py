import clr
import os
from aacommpy.category import categories

path = os.path.join(os.path.dirname(__file__), 'AAComm.dll')
clr.AddReference(path)

for category in categories:
    if category["enable"]:
        exec(f"from {category['from']} import {category['name']}")

# Add the imported categories to __all__
__all__ = [category["name"] for category in categories if category["enable"]]
