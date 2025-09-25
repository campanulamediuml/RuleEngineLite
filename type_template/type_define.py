from typing import TypedDict, List

TypeDataKey = str
TypeExpr = str


class ConfigFile(TypedDict):
    data_keys: List[TypeDataKey]
    rules: List[TypeExpr]
