from typing import Any


class JSONSerializableMixin:
    def to_json(self) -> dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}  # type: ignore


def remove_urn(id: str) -> str:
    if 'urn:uuid:' in id:
        return id.split(":")[-1]
    return id
