"""
为整个工程提供统一的绝对路径
"""

import os

# def get_project_root() -> str:
#     """
#     获取工程所在的根目录
#     Returns:
#         str: 工程根目录的绝对路径
#     """
#     current_file_path = os.path.abspath(__file__)
#     current_dir = os.path.dirname(current_file_path)
#     project_root = os.path.dirname(current_dir)
#     return project_root
#
# def get_abs_path(relative_path: str) -> str:
#     """
#     将相对路径转换为绝对路径
#     Args:
#         relative_path (str): 相对路径
#     Returns:
#         str: 绝对路径
#     """
#     project_root = get_project_root()
#     abs_path = os.path.join(project_root, relative_path)
#     return abs_path


def get_abs_path(relative_path: str) -> str:
    """
    将相对路径转换为绝对路径
    Args:
        relative_path (str): 相对路径
    Returns:
        str: 绝对路径
    """
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, relative_path)

if __name__ == "__main__":
    # 测试 get_abs_path 函数
    relative_path = "data/sample.txt"
    abs_path = get_abs_path(relative_path)
    print(f"Relative path: {relative_path}")
    print(f"Absolute path: {abs_path}")