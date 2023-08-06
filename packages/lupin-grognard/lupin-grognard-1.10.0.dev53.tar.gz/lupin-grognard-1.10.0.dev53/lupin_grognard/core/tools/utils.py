import logging
import os
import re
import sys
from typing import List

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.config import (
    COMMIT_DELIMITER,
    INITIAL_COMMIT,
    MAIN_BRANCHES_LIST,
)
from lupin_grognard.core.git import Git


def read_file(file: str) -> str:
    with open(f"{file}", "r", encoding="utf-8") as file:
        data = file.read()
        return data


def write_file(file: str, content: str):
    with open(f"{file}", "w", encoding="utf-8") as outfile:
        outfile.write(content)


def get_version():
    """get version from setup.cfg file and
    update __version__ in lupin_grognard.__init__.py
    """
    setup_cfg = read_file("setup.cfg")
    _version = re.search(
        r"(^version = )(\d{1,2}\.\d{1,2}\.\d{1,2})(\.[a-z]{1,})?(\d{1,2})?",
        setup_cfg,
        re.MULTILINE,
    )
    version = ""
    for group in _version.group(2, 3, 4):
        if group is not None:
            version = version + str(group)
    content = f'__version__ = "{version}"\n'
    write_file(file="lupin_grognard/__init__.py", content=content)
    return version


def get_current_branch_name() -> str:
    branch_name = Git().get_branch_name()
    # branch name can be messing if running in CI
    if not branch_name:
        branch_name = os.getenv("CI_COMMIT_BRANCH")
    if not branch_name:
        branch_name = os.getenv("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME")
    if not branch_name:
        return ""
    return branch_name


def display_supported_commit_types() -> None:
    commit_type = [
        "build(add|change|remove)",
        "bump",
        "ci",
        "deps(add|change|remove)",
        "docs",
        "enabler",
        "feat(add|change|remove)",
        "fix",
        "refactor",
        "test",
    ]
    print("Supported commit types: " + ", ".join(commit_type))
    print(
        'Only one major commit types allowed per branch: "enabler", "feat", "fix" or "refactor".'
    )


def display_number_of_commits_to_check(commits: List[Commit]):
    number_commits_to_check = len(commits)
    if number_commits_to_check == 0:
        print("0 commit to check")
        sys.exit(0)
    elif number_commits_to_check == 1:
        print(f"Found {number_commits_to_check} commit to check:")
    else:
        print(f"Found {number_commits_to_check} commits to check:")


def generate_commit_list(commits_string: str) -> List[Commit]:
    """Geneartes the list of commits from Git().get_log().stdout value"""
    return [
        Commit(commit)
        for commit in commits_string.split(COMMIT_DELIMITER)
        if len(commit) > 0
    ]


def generate_commits_range_to_check(
    branch_list: List[str],
    commits: List[Commit],
    ci_mr_target_branch_name: str = "",
    initial_commits: List[str] = INITIAL_COMMIT,
) -> List:
    """
    generates a list of message ranges starting with INITIAL_COMMIT
    or the last merge into a branch contained in the branch list

    If ci_mr_target_branch_name eqal main, the function returns the commit range
    starting from the second merge found.
    """
    merge_count = 0
    merge_result_pipeline = False

    for index, commit in enumerate(commits):
        if (
            commit.title.startswith("Merge branch")
            and ci_mr_target_branch_name in ["main", "master"]
            and index == 0
        ):
            merge_result_pipeline = True

        if merge_result_pipeline:
            if commit.title.startswith("Merge branch"):
                merge_count += 1
                if merge_count == 2:
                    return commits[:index]
        else:
            if commit.title.startswith("Merge branch"):
                for branch in branch_list:
                    if commit.title.endswith(f"into '{branch}'"):
                        return commits[:index]
            elif commit.title in initial_commits:
                return commits[:index]
    return list()


# from lupin_grognard.core.commit.commit_validator import CheckModes

# def generate_commits_range(mode_check: CheckModes, all_checks: bool, ci_mr_target_branch_name: str, current_branch_name: str, git_log: Git):
#     if mode_check == mode_check.ALL_CHECKS_WITH_JAMA or mode_check == mode_check.ALL_CHECKS_WITHOUT_JAMA:
#         if not all_checks:
#             info(
#                 msg=f"Processing all commits since current branch '{current_branch_name}' is a main one"
#             )
#         else:
#             info(
#                 msg=f"Processing all commits since initial commit as --all option is set"
#             )

#         commits = generate_commit_list(git_log.stdout)

#         if ci_mr_target_branch_name in ["main", "master"]:
#             info(
#                 msg="Processing check-commits for a pipeline merge request to a main branch target"
#             )
#             commits = generate_commits_range_to_check(
#                 branch_list=MAIN_BRANCHES_LIST,
#                 commits=commits,
#                 ci_mr_target_branch_name=ci_mr_target_branch_name,
#             )

#     if mode_check == mode_check.NORMAL_CHECKS:
#         git_log = git.get_log(max_line_count=50, first_parent=True)
#         commits = generate_commit_list(git_log.stdout)
#         commits = generate_commits_range_to_check(
#             branch_list=MAIN_BRANCHES_LIST,
#             commits=commits,
#         )


def die(msg: str) -> None:
    logging.error(msg)
    sys.exit(1)


def warn(msg: str) -> None:
    logging.warning(msg)


def info(msg: str) -> None:
    logging.info(msg)


def check_if_file_exists(file: str) -> bool:
    file_path = os.path.join(os.getcwd(), file)
    return os.path.isfile(file_path)


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )


def is_main_branch(branch_name: str, main_branch_list: List) -> bool:
    return branch_name in main_branch_list
