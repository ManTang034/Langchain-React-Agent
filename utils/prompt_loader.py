from utils.config_handler import prompts_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path


def load_system_prompt():
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}. Please check the prompts configuration.")
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"Error loading system prompt: {str(e)}")
        raise e

def load_rag_prompt():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_path"])
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}. Please check the prompts configuration.")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"Error loading rag_summarize prompt: {str(e)}")
        raise e


def load_report_prompt():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}. Please check the prompts configuration.")
        raise e

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"Error loading report prompt: {str(e)}")
        raise e

if __name__ == "__main__":
    print(load_system_prompt())