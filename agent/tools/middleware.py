from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import (ModelRequest, after_agent,
                                         after_model, before_agent,
                                         before_model, dynamic_prompt,
                                         wrap_model_call, wrap_tool_call)
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger
from utils.prompt_loader import load_report_prompt, load_system_prompt


@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    logger.info(f"[tool monitor]执行工具:{request.tool_call['name']}")
    logger.info(f"[tool monitor]工具参数:{request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}执行结果:{result}")

        if request.tool_call['name'] == "fill_external_data":
            request.runtime.context["report"] = True
        return result
    except Exception as e:
        logger.error(f"[tool monitor]工具{request.tool_call['name']}执行出错:{e}")
        raise e

@before_model
def log_before_model(
    state:AgentState,
    runtime:Runtime
):
    logger.info(f"[log_before_model]模型执行前，agent_state中有{len(state['messages'])}条消息")

    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content}")

    return None

@dynamic_prompt
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get("report", False)
    if is_report:
        return load_report_prompt()

    return load_system_prompt()