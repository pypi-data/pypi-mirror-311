from typing import TypedDict


class DesiredWorkerLabel(TypedDict):
    value: str | int
    required: bool | None = None
    weight: int | None = None
    comparator: int | None = (
        None  # _ClassVar[WorkerLabelComparator] TODO figure out type
    )
