import dataclasses


@dataclasses.dataclass
class CutSource:
    object_id: str
    affected_fields: list[str]
