from __future__ import annotations
import sys
from pathlib import Path

ZUT_ROOT = Path(__file__).parent
""" Root directory of `zut` library """


def is_list_or_tuple_of(instance, element_type: type|tuple[type]):
    if not isinstance(instance, (list,tuple)):
        return False

    for element in instance:
        if not isinstance(element, element_type):
            return False
        
    return True
