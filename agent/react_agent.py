from agent.tools.agent_tools import (fetch_external_data,
                                     fill_context_for_report,
                                     generate_external_data, get_current_month,
                                     get_user_id, get_user_location,
                                     get_weather, rag_summarize)
from agent.tools.middleware import (log_before_model, monitor_tool,
                                    report_prompt_switch)
from langchain.agents import create_agent
from model.factory import chat_model_factory
from utils.prompt_loader import load_system_prompt


class ReActAgent:
    def __init__(self):
        self.agent = create_agent(
            model = chat_model_factory,
            system_prompt = load_system_prompt(),
            tools = [rag_summarize, get_weather, get_user_location, get_user_id, get_current_month, generate_external_data, fetch_external_data, fill_context_for_report],
            middleware = [monitor_tool, log_before_model, report_prompt_switch]
        )

    def execute_stream(self,query:str):
        input_dict = {
            "messages":[{"role":"user","content":query}],
        }

        for chunk in self.agent.stream(input_dict,stream_mode="values",context={"report":False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"

if __name__ == "__main__":
    agent = ReActAgent()

    for chunk in agent.execute_stream("给我生成使用报告"):
        print(chunk, end="", flush=True)