from functools import wraps
import inspect
import json
from typing import Callable

from arcadepy import Arcade
from arcade.core.schema import ToolContext
from agents.run_context import RunContextWrapper


def replace_arcade_context_with_openai_context(arcade_tool_func: Callable, openai_tool_func: Callable):
    # Get the original signature
    sig = inspect.signature(arcade_tool_func)
    params = list(sig.parameters.values())

    # Find and replace the context parameter
    new_params = []
    context_param_found = False

    for param in params:
        if param.annotation == ToolContext:
            # Replace this parameter's annotation with RunContextWrapper
            context_param_found = True
            new_param = inspect.Parameter(
                param.name,
                param.kind,
                default=param.default,
                annotation=RunContextWrapper
            )
            new_params.append(new_param)
        else:
            new_params.append(param)

    if context_param_found:
        openai_tool_func.__signature__ = sig.replace(parameters=new_params)

        # Update the annotations dictionary
        original_annotations = getattr(arcade_tool_func, '__annotations__', {})
        new_annotations = {k: v for k, v in original_annotations.items()}

        # Find the context parameter name
        for param in params:
            if param.annotation == ToolContext:
                new_annotations[param.name] = RunContextWrapper
                break

        openai_tool_func.__annotations__ = new_annotations


def arcade_to_openai_tool_adapter(
    arcade_tool_func: Callable,
    arcade_tool_name: str,
):
    if arcade_tool_name.startswith("Arcade"):
        arcade_tool_name = arcade_tool_name[6:]

    @wraps(arcade_tool_func)
    async def adapted_arcade_tool(context: RunContextWrapper, args_json: str):
        client = Arcade()
        auth_response = client.tools.authorize(
            tool_name=arcade_tool_name,
            user_id=context.context["user_id"],
        )

        if auth_response.status != "completed":
            print(f"Click this link to authorize: {auth_response.url}")

        client.auth.wait_for_completion(auth_response)

        print(f"Executing Arcade tool {arcade_tool_name} with input {args_json}")

        response = client.tools.execute(
            tool_name=arcade_tool_name,
            input=json.loads(args_json),
            user_id=context.context["user_id"],
        )

        if isinstance(response, str):
            return response

        try:
            return json.dumps(response)
        except Exception:
            return str(response)

    replace_arcade_context_with_openai_context(arcade_tool_func, adapted_arcade_tool)

    return adapted_arcade_tool
