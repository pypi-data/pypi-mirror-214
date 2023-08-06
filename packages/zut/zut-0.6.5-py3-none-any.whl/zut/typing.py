from __future__ import annotations
import sys


if sys.version_info[0:2] < (3, 8):
    from typing_extensions import Literal, Protocol
else:
    from typing import Literal, Protocol
    
if sys.version_info[0:2] < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self
