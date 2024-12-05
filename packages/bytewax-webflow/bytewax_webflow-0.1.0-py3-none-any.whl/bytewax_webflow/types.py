from dataclasses import dataclass, field
from typing import Any


@dataclass
class WebflowCollectionItem:
    name: str
    slug: str
    is_archived: bool = False
    is_draft: bool = False
    fields: dict[str, Any] = field(default_factory=dict)
    id: str | None = None


@dataclass
class WebflowCollectionField:
    slug: str
    is_required: bool
    is_editable: bool
