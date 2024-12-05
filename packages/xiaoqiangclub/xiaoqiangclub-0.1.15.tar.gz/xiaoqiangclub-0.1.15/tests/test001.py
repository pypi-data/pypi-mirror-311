import re


def get_repo_name_from_url(repo_url: str) -> str:
    """
    从 Git 仓库地址中提取项目名称

    :param repo_url: Git 仓库地址
    :return: 仓库名称（例如：`repo`）
    """
    # 匹配仓库地址中的最后一部分作为项目名称（去掉 .git 后缀）
    match = re.search(r'([a-zA-Z0-9_-]+)(?=\.git$)', repo_url)
    if match:
        return match.group(0)
    return "git_auto_runner"  # 如果提取失败，返回默认名称


print(get_repo_name_from_url('https://github.com/username/repo.git'))