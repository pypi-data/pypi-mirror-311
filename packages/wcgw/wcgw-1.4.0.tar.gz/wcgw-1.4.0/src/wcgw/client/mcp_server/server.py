import asyncio
import importlib
import json
import os
import traceback
from typing import Any

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.types import Tool as ToolParam
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl, ValidationError
import mcp.server.stdio
from ..tools import DoneFlag, get_tool_output, which_tool_name, default_enc
from ...types_ import (
    BashCommand,
    BashInteraction,
    CreateFileNew,
    FileEdit,
    ReadFile,
    ReadImage,
    ResetShell,
    Initialize,
)


server = Server("wcgw")


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    return []


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    raise ValueError("No resources available")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return []


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    types.GetPromptResult(messages=[])


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """

    with open(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "diff-instructions.txt"
        )
    ) as f:
        diffinstructions = f.read()
    return [
        ToolParam(
            inputSchema=Initialize.model_json_schema(),
            name="Initialize",
            description="""
- Always call this at the start of the conversation before anything else.
""",
        ),
        ToolParam(
            inputSchema=BashCommand.model_json_schema(),
            name="BashCommand",
            description="""
- Execute a bash command. This is stateful (beware with subsequent calls).
- Do not use interactive commands like nano. Prefer writing simpler commands.
- Status of the command and the current working directory will always be returned at the end.
- Optionally `exit shell has restarted` is the output, in which case environment resets, you can run fresh commands.
- The first line might be `(...truncated)` if the output is too long.
- Always run `pwd` if you get any file or directory not found error to make sure you're not lost.
- The control will return to you in 5 seconds regardless of the status. For heavy commands, keep checking status using BashInteraction till they are finished.
""",
        ),
        ToolParam(
            inputSchema=BashInteraction.model_json_schema(),
            name="BashInteraction",
            description="""
- Interact with running program using this tool
- Special keys like arrows, interrupts, enter, etc.
- Send text input to the running program.
- Send send_specials=["Enter"] to recheck status of a running program.
- Only one of send_text, send_specials, send_ascii should be provided.
""",
        ),
        ToolParam(
            inputSchema=ReadFile.model_json_schema(),
            name="ReadFile",
            description="""
- Read full file content
- Provide absolute file path only
""",
        ),
        ToolParam(
            inputSchema=CreateFileNew.model_json_schema(),
            name="CreateFileNew",
            description="""
- Write content to a new file. Provide file path and content. Use this instead of BashCommand for writing new files.
- This doesn't create any directories, please create directories using `mkdir -p` BashCommand.
- Provide absolute file path only.
- For editing existing files, use FileEdit instead of this tool.
""",
        ),
        ToolParam(
            inputSchema=ReadImage.model_json_schema(),
            name="ReadImage",
            description="Read an image from the shell.",
        ),
        ToolParam(
            inputSchema=ResetShell.model_json_schema(),
            name="ResetShell",
            description="Resets the shell. Use only if all interrupts and prompt reset attempts have failed repeatedly.",
        ),
        ToolParam(
            inputSchema=FileEdit.model_json_schema(),
            name="FileEdit",
            description="""
- Use absolute file path only.
- Use SEARCH/REPLACE blocks to edit the file.
"""
            + diffinstructions,
        ),
        ToolParam(
            inputSchema=ReadImage.model_json_schema(),
            name="ReadImage",
            description="""
- Read an image from the shell.
""",
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if not arguments:
        raise ValueError("Missing arguments")

    tool_type = which_tool_name(name)

    try:
        tool_call = tool_type(**arguments)
    except ValidationError:

        def try_json(x: str) -> Any:
            try:
                return json.loads(x)
            except json.JSONDecodeError:
                return x

        tool_call = tool_type(**{k: try_json(v) for k, v in arguments.items()})

    try:
        output_or_done, _ = get_tool_output(
            tool_call, default_enc, 0.0, lambda x, y: ("", 0), 8000
        )

    except Exception as e:
        output_or_done = f"GOT EXCEPTION while calling tool. Error: {e}"
        tb = traceback.format_exc()
        print(output_or_done + "\n" + tb)

    assert not isinstance(output_or_done, DoneFlag)
    if isinstance(output_or_done, str):
        if issubclass(tool_type, Initialize):
            output_or_done += """
            
You're an expert software engineer with shell and code knowledge.

Instructions:
   
    - You should use the provided bash execution, reading and writing file tools to complete objective.
    - First understand about the project by getting the folder structure (ignoring .git, node_modules, venv, etc.)
    - Always read relevant files before editing.
    - Do not provide code snippets unless asked by the user, instead directly edit the code.

    
Additional instructions:
    Always run `pwd` if you get any file or directory not found error to make sure you're not lost, or to get absolute cwd.

    Always write production ready, syntactically correct code.
"""

        return [types.TextContent(type="text", text=output_or_done)]

    return [
        types.ImageContent(
            type="image",
            data=output_or_done.data,
            mimeType=output_or_done.media_type,
        )
    ]


async def main() -> None:
    version = importlib.metadata.version("wcgw")
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="wcgw",
                server_version=version,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
