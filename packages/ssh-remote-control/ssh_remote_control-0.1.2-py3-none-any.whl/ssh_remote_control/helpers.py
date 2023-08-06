from __future__ import annotations

import slugify


def name_to_key(name: str) -> str:
    """Name to key."""
    return slugify.slugify(name, separator="_")
