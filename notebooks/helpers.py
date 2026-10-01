"""Pure helpers shared by the notebooks (unit-testable without Spark)."""
import re

LAKE = "abfss://{container}@<storageaccount>.dfs.core.windows.net"


def to_snake_case(name: str) -> str:
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name.strip())
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return re.sub(r"_+", "_", name).strip("_").lower()


def parse_keys(keys: str) -> list[str]:
    return [to_snake_case(k) for k in keys.split(",") if k.strip()]


def layer_path(layer: str, source_system: str, table: str) -> str:
    if layer not in {"bronze", "silver", "gold"}:
        raise ValueError(f"unknown layer {layer}")
    return f"{LAKE.format(container=layer)}/{source_system.lower()}/{table.lower()}"


ORACLE_TYPE_MAP = {"NUMBER": "decimal(38,10)", "VARCHAR2": "string", "DATE": "timestamp", "CLOB": "string"}


def spark_type_for(source_type: str) -> str:
    return ORACLE_TYPE_MAP.get(source_type.upper().split("(")[0], "string")
