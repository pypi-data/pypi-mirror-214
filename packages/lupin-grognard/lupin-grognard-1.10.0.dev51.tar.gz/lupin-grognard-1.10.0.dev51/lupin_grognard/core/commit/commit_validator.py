import re
from enum import Enum
from typing import List, Tuple

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.commit.commit_error import BodyError, ErrorCount
from lupin_grognard.core.commit.commit_reporter import CommitReporter
from lupin_grognard.core.config import (
    COMMIT_TYPE_MUST_HAVE_SCOPE,
    COMMIT_TYPE_MUST_NOT_HAVE_SCOPE,
    COMMIT_WITH_SCOPE,
    INITIAL_COMMIT,
    JAMA_REGEX,
    MAX_COMMIT_DESCR_LINES,
    MIN_COMMIT_DESCR_LENTH,
    PATTERN,
    TITLE_FAILED,
)


class CheckModes(Enum):
    ALL_CHECKS_WITH_JAMA = 1
    ALL_CHECKS_WITHOUT_JAMA = 2
    NORMAL_CHECKS = 3


class CommitsCheckModes:
    def __init__(
        self, current_branch: str, ci_mr_target_branch: str, all_checks_flag: bool
    ):
        self._current_branch = current_branch
        self._ci_mr_target_branch = ci_mr_target_branch
        self._all_checks_flag = all_checks_flag  # rename to all_check_commits

    def mode(self) -> CheckModes:
        main_branches = ["main", "master"]
        dev_branches = ["dev", "develop", "development"]
        if (
            self._current_branch in main_branches
            or self._ci_mr_target_branch in main_branches
        ):
            return CheckModes.ALL_CHECKS_WITH_JAMA
        elif (
            self._current_branch in dev_branches
            or self._ci_mr_target_branch in dev_branches
            or self._all_checks_flag
        ):
            return CheckModes.ALL_CHECKS_WITHOUT_JAMA
        else:
            return CheckModes.NORMAL_CHECKS


class CommitValidator(Commit):
    def __init__(
        self,
        commit: Commit,
        error_counter: ErrorCount,
        mode_check: CheckModes,
    ):
        super().__init__(commit=commit.commit)
        self.reporter = CommitReporter(commit=commit)
        self.error_counter = error_counter
        self.mode_check = mode_check

    def perform_checks(self) -> None:
        if (
            self.mode_check == CheckModes.ALL_CHECKS_WITH_JAMA
            or self.mode_check == CheckModes.ALL_CHECKS_WITHOUT_JAMA
        ):
            if self._is_merge_commit(self.title):
                if not self._validate_commit_merge():
                    self.error_counter.increment_merge_error()
            else:
                if not self._validate_commit_title():
                    self.error_counter.increment_title_error()

                if self.mode_check == CheckModes.ALL_CHECKS_WITH_JAMA:
                    if not self._validate_body(jama_check=True):
                        self.error_counter.increment_body_error()
                else:
                    if not self._validate_body():
                        self.error_counter.increment_body_error()

        if self.mode_check == CheckModes.NORMAL_CHECKS:
            if not self._validate_commit_title():
                self.error_counter.increment_title_error()
            if not self._is_merge_commit(self.title):
                if not self._validate_body():
                    self.error_counter.increment_body_error()

    def _validate_commit_title(self) -> bool:
        if self._validate_commit_message(self.title, self.type, self.scope):
            self.reporter.display_valid_title_report()
            return True
        else:
            return False

    def _validate_body(self, jama_check: bool = False) -> bool:
        body_error = BodyError(
            is_conventional=[],
            descr_is_too_short=[],
            num_empty_line=0,
            invalid_body_length=False,
            jama_not_referenced=False,
            duplicate_jama_line=False,
            duplicate_jama_refs=[],
            invalid_jama_refs=False,
        )

        if jama_check:
            self._validate_jama_referencing(body_error=body_error)

        if self.body:
            if not self._is_commit_body_length_valid():
                body_error.invalid_body_length = True

            for message in self.body:
                if self._is_conventional_commit_body_valid(message=message):
                    body_error.is_conventional.append(
                        message
                    )  # must not start with a conventional message
                if not self._is_commit_body_line_length_valid(message=message):
                    if message != "":
                        body_error.descr_is_too_short.append(message)
                    else:
                        body_error.num_empty_line += 1
        if any(
            [
                body_error.is_conventional,
                body_error.descr_is_too_short,
                body_error.num_empty_line > 0,
                body_error.invalid_body_length,
                body_error.jama_not_referenced,
                body_error.duplicate_jama_line,
                body_error.duplicate_jama_refs,
                body_error.invalid_jama_refs,
            ]
        ):
            self.reporter.display_body_report(body_error=body_error)
            return False
        return True

    def _validate_jama_referencing(self, body_error: BodyError) -> None:
        if not self._is_last_description_line_startswith_jama():
            body_error.jama_not_referenced = True
        else:
            if not self._is_sigle_line_startswith_jama_reference():
                body_error.duplicate_jama_line = True

        if (
            self._is_last_description_line_startswith_jama()
            and self.title not in INITIAL_COMMIT
        ):
            (
                duplicate_jama_refs,
                invalid_jama_refs,
            ) = self._validate_jama_items()
            if duplicate_jama_refs:
                body_error.duplicate_jama_refs = duplicate_jama_refs
            if invalid_jama_refs:
                body_error.invalid_jama_refs = invalid_jama_refs

    def _validate_commit_message(self, commit_msg: str, type: str, scope: str) -> bool:
        if self._is_special_commit(commit_msg=commit_msg):
            return True

        match type:
            case None:
                self.reporter.display_invalid_title_report(error_message=TITLE_FAILED)
                return False
            case match_type if (match_type := type) in COMMIT_WITH_SCOPE:
                return self._validate_commit_message_for_specific_type(
                    scope=scope, type=match_type
                )
            case _:
                return self._validate_commit_message_for_generic_type(
                    type=type, scope=scope
                )

    def _is_conventional_commit_body_valid(self, message: str) -> bool:
        """Checks if the line in the body of a commit message starts with a conventional commit"""
        return bool(re.match(PATTERN, message))

    def _is_commit_body_line_length_valid(self, message: str) -> bool:
        """Checks if the body line is not less than MIN_COMMIT_DESCR_LENTH"""
        return len(message) >= MIN_COMMIT_DESCR_LENTH

    def _is_commit_body_length_valid(self) -> bool:
        """Checks if the body length is not greater than MAX_COMMIT_DESCR_LINES"""
        return len(self.body) <= MAX_COMMIT_DESCR_LINES

    def _validate_jama_items(self) -> Tuple[List[str], List[str]]:
        jama_ref_line = self.body[-1]
        jama_refs = jama_ref_line.replace("JAMA:", "").strip().split(" ")
        unique_jama_refs = set()
        duplicate_jama_refs = []
        invalid_jama_refs = []

        for jama_ref in jama_refs:
            if not re.match(JAMA_REGEX, jama_ref):
                invalid_jama_refs.append(jama_ref)
            elif jama_ref in unique_jama_refs and jama_ref not in duplicate_jama_refs:
                duplicate_jama_refs.append(jama_ref)
            else:
                unique_jama_refs.add(jama_ref)
        return duplicate_jama_refs, invalid_jama_refs

    def _is_special_commit(self, commit_msg: str) -> bool:
        """Checks if the commit is a Merge or in the list of initial commits"""
        return commit_msg.startswith("Merge") or commit_msg in INITIAL_COMMIT

    def _is_merge_commit(self, commit_msg: str) -> bool:
        return commit_msg.startswith("Merge")

    def _validate_commit_merge(self) -> bool:
        self.reporter.display_merge_report(approvers=self.approvers)
        if len(self.approvers) < 1:
            return False
        return True

    def _validate_commit_message_for_specific_type(self, scope: str, type: str) -> bool:
        """
        Validates the scope for a COMMIT_WITH_SCOPE list.
        If the scope is (change) then the commit title and description
        must not contain the words 'remove' or 'removed'
        """
        if scope is None or scope not in ["(add)", "(change)", "(remove)"]:
            self.reporter.display_invalid_title_report(
                error_message=COMMIT_TYPE_MUST_HAVE_SCOPE.format(type=type)
            )
            return False
        else:
            if scope == "(change)":
                return self._validate_change_scope_without_remove_word()
            return True

    def _contains_remove_words(self, text: str) -> bool:
        """Checks if the text contains the words 'remove' or 'removed'"""
        words = text.lower().split(" ")
        return any(str in words for str in ["remove", "removed"])

    def _validate_change_scope_without_remove_word(self):
        """
        Validate that a commit with the scope (change) does not contain the words
        'remove' and 'removed' in the title or description
        """
        full_text = self.title + " " + " ".join(self.body) if self.body else self.title
        if self._contains_remove_words(text=full_text):
            self.reporter.display_invalid_title_report(
                error_message=(
                    "Found a commit message that talks about removing something while given "
                    "scope is 'change': change scope to 'remove' or update the commit description"
                )
            )
            return False
        return True

    def _validate_commit_message_for_generic_type(self, type, scope: str) -> bool:
        """Validates other commit types do not contain a scope"""
        if scope is None:
            return True
        else:
            error_message = COMMIT_TYPE_MUST_NOT_HAVE_SCOPE.format(type, type)
            self.reporter.display_invalid_title_report(error_message=error_message)
            return False
