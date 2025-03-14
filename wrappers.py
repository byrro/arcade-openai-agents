from types import ModuleType
from typing import Callable

from arcade.core.catalog import ToolCatalog
from agents.function_schema import function_schema
from agents.tool import FunctionTool
from adapters import arcade_to_openai_tool_adapter


def arcade_tool_wrapper(tool_func: Callable, toolkit_name: str) -> FunctionTool:
    catalog = ToolCatalog()
    arcade_tool_definition = catalog.create_tool_definition(tool_func, toolkit_name)

    adapted_arcade_tool_func = arcade_to_openai_tool_adapter(tool_func, arcade_tool_definition.fully_qualified_name)

    openai_tool_schema = function_schema(
        func=adapted_arcade_tool_func,
        name_override=arcade_tool_definition.name,
        description_override=arcade_tool_definition.description,
    )

    return FunctionTool(
        name=arcade_tool_definition.name,
        description=arcade_tool_definition.description,
        params_json_schema=openai_tool_schema.params_json_schema,
        on_invoke_tool=adapted_arcade_tool_func,
        strict_json_schema=True,
    )


def arcade_toolkit_wrapper(toolkit: ModuleType) -> list[FunctionTool]:
    catalog = ToolCatalog()
    catalog.add_module(toolkit)

    return [
        arcade_tool_wrapper(tool.tool, tool.definition.toolkit.name)
        for tool in catalog._tools.values()
    ]
