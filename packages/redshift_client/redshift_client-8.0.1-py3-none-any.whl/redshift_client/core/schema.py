from .table import (
    Table,
)
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    FrozenDict,
)
from redshift_client.core.id_objs import (
    TableId,
)
from typing import (
    Literal,
    Union,
)


@dataclass(frozen=True)
class Schema:
    tables: FrozenDict[TableId, Table]


class QuotaUnit(Enum):
    MB = "MB"
    GB = "GB"
    TB = "TB"


@dataclass(frozen=True)
class Quota:
    value: int
    unit: QuotaUnit


@dataclass(frozen=True)
class SchemaPolicy:
    owner: str
    quota: Union[Quota, Literal["UNLIMITED"]]
