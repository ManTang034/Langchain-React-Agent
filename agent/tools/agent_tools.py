import os
import random

from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path

rag = RagSummarizeService()

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]
external_data = {}
@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str)-> str:
    """
    从向量存储中检索参考资料，并将提问和参考资料提交给模型，让模型总结回复
    """
    return rag.rag_summarize(query=query, top_k=3)

@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str)-> str:
    """
    获取指定城市的天气，以消息字符串的形式返回
    """
    # 这里可以调用实际的天气 API 获取天气信息，这里为了演示，直接返回一个模拟的天气信息
    return f"{city}的天气是晴天，温度25摄氏度，湿度60%，风速5米/秒。"

@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location()-> str:
    return random.choice(["北京", "上海", "广州", "深圳", "杭州", "成都", "重庆", "武汉", "西安", "南京"])

@tool(description="获取用户的唯一标识符，以纯字符串形式返回")
def get_user_id()-> str:
    return random.choice(user_ids)

@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month()-> str:
    return random.choice(month_arr)

def generate_external_data():
    """
    {
        "user_id": {
                "month":{"特征":xxx, "效率":xxx, ...}
                "month":{"特征":xxx, "效率":xxx, ...}
                "month":{"特征":xxx, "效率":xxx, ...}
                ...
        },
        "user_id": {
                "month":{"特征":xxx, "效率":xxx, ...}
                "month":{"特征":xxx, "效率":xxx, ...}
                "month":{"特征":xxx, "效率":xxx, ...}
                ...
        },
        "user_id": {
                "month":{"特征":xxx, "效率":xxx, ...}
                "month":{"特征":xxx, "效率":xxx, ...}
                "month":{"特征":xxx, "效率":xxx, ...}
                ...
        },
        ...
    }
    :return:
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件不存在: {external_data_path}")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr:list[str] = line.strip().split(",")

                user_id = arr[0].replace('"', '')
                feature = arr[1].replace('"', '')
                efficiency = arr[2].replace('"', '')
                consumables = arr[3].replace('"', '')
                comparison = arr[4].replace('"', '')
                time = arr[5].replace('"', '')

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison
                }


@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回，如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str)-> str:
    """
    从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回，如果未检索到返回空字符串
    :param user_id: 用户唯一标识符
    :param month: 月份，格式为 YYYY-MM
    :return: 使用记录，以纯字符串形式返回，如果未检索到返回空字符串
    """
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"未检索到用户 {user_id} 在 {month} 的使用记录")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report工具调用成功"

if __name__ == "__main__":
    print(fetch_external_data("1021", "2025-01"))