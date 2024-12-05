from typing import Any, Sequence
from urllib.parse import urljoin

import requests

from .types import WebflowCollectionItem, WebflowCollectionField


DEFAULT_BASE_URL = "https://api.webflow.com/v2/"


class WebflowClient:
    def __init__(self, access_token: str, base_url: str | None = None):
        self._access_token = access_token
        self._base_url = base_url if base_url is not None else DEFAULT_BASE_URL

    def _request(
        self, method: str, path: str, *, params: dict[str, Any] | None = None, data=None
    ):
        response = requests.request(
            method,
            urljoin(self._base_url, path),
            headers={
                "Authorization": f"Bearer {self._access_token}",
            },
            params=params,
            json=data,
        )

        if not response.ok:
            raise ValueError(
                f"Unable to {method} {path}: {response.status_code} {response.text}"
            )

        return response.json()

    @staticmethod
    def _parse_collection_item(data) -> WebflowCollectionItem:
        fields = data.get("fieldData") or {}

        name = fields.pop("name")
        slug = fields.pop("slug")

        return WebflowCollectionItem(
            id=data["id"],
            name=name,
            slug=slug,
            is_archived=data.get("isArchived", False),
            is_draft=data.get("isDraft", False),
            fields=fields,
        )

    @staticmethod
    def _serialize_collection_item(value: WebflowCollectionItem):
        return {
            "id": value.id,
            "isArchived": value.is_archived,
            "isDraft": value.is_draft,
            "fieldData": {
                **value.fields,
                "name": value.name,
                "slug": value.slug,
            },
        }

    def get_item_by_slug(
        self, collection_id: str, slug: str
    ) -> WebflowCollectionItem | None:
        data = self._request(
            "GET", f"collections/{collection_id}/items", params={"slug": slug}
        )

        if len(data["items"]) == 0:
            return None

        return self._parse_collection_item(data["items"][0])

    @staticmethod
    def _parse_collection_field(data) -> WebflowCollectionField:
        return WebflowCollectionField(
            slug=data["slug"],
            is_required=data["isRequired"],
            is_editable=data["isEditable"],
        )

    def get_collection_schema(
        self, collection_id: str
    ) -> Sequence[WebflowCollectionField]:
        collection = self._request("GET", f"collections/{collection_id}")

        return [self._parse_collection_field(f) for f in collection["fields"]]

    def insert_collection_items(
        self, collection_id: str, items: Sequence[WebflowCollectionItem]
    ):
        self._request(
            "POST",
            f"collections/{collection_id}/items",
            data={
                "items": [self._serialize_collection_item(i) for i in items],
            },
        )

    def update_collection_items(
        self, collection_id: str, items: Sequence[WebflowCollectionItem]
    ):
        self._request(
            "POST",
            f"collections/{collection_id}/items",
            data={
                "items": [self._serialize_collection_item(i) for i in items],
            },
        )


__all__ = ("WebflowClient",)
