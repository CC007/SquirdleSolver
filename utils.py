from typing import Any

def sort_dict_by_key(d: dict[Any, Any], desc=True) -> dict[Any, Any]:
    return dict(sorted(d.items(), reverse=desc))

def sort_dict_by_val(d: dict[Any, Any], desc=True) -> dict[Any, Any]:
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=desc))