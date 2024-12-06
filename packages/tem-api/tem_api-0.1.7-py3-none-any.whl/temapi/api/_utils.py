from typing import Any, Dict


def build_url(base: str, args: Dict[str, Any]):
    params = list()

    for key, value in args.items():
        value = "" if value is None else value
        params.append(f"{key}={value}")

    if len(params) > 0:
        qs = "&".join(params)
        return f"{base}?{qs}"
    else:
        return base
