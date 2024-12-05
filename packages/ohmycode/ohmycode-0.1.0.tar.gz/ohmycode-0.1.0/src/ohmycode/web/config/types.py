from typing import TypedDict


class ToolOptionValue(TypedDict):
    type: str
    value: str | bool | int | list[str]
    choices: list[str] | None
    choices_desc: dict[str, str] | None


class ToolOption(TypedDict):
    name: str
    description: str
    value: ToolOptionValue


class ToolConfig(TypedDict):
    name: str
    description: str
    enabled: bool
    command: str
    options: dict[str, ToolOption] 