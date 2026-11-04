"""Tests de la pile et de l'analyse de parenthèses (TP 1, exercice 2)."""

import pytest

from sda.tp01_data_structures.stack import (
    BracketReport,
    Stack,
    analyse,
    analyse_file,
    analyse_text,
)


def test_stack_lifo_order():
    stack = Stack()
    assert stack.is_empty()
    for value in (1, 2, 3):
        stack.push(value)
    assert stack.size == 3
    assert stack.peek() == 3
    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1
    assert stack.is_empty()


def test_stack_errors():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()
    with pytest.raises(IndexError):
        stack.peek()


def test_stack_repr():
    stack = Stack()
    stack.push("a")
    stack.push("b")
    assert repr(stack) == "Stack(['b', 'a'])"


@pytest.mark.parametrize(
    "expression",
    ["", "()", "[]", "{}", "<>", "{[()]}", "<a(b)[c]{d}>", "no brackets here"],
)
def test_valid_expressions(expression):
    assert analyse(expression)
    assert analyse_text(expression).valid


@pytest.mark.parametrize(
    "expression",
    ["(", ")", "(]", "([)]", "{<}>", "(()", "())", "a(b]c"],
)
def test_invalid_expressions(expression):
    assert not analyse(expression)
    assert not analyse_text(expression).valid


def test_ignores_non_bracket_characters():
    assert analyse("if (a != b) { return [a, b]; } // comment")


def test_reports_unexpected_closing_bracket():
    report = analyse_text("abc\n  ]")
    assert not report
    assert report.line == 2
    assert report.column == 3
    assert report.character == "]"
    assert "inattendue" in report.message


def test_reports_mismatched_bracket():
    report = analyse_text("(abc]")
    assert not report
    assert report.line == 1
    assert report.column == 5
    assert report.character == "]"
    assert "ouvert à la ligne 1" in report.message


def test_reports_unclosed_bracket_at_its_own_position():
    report = analyse_text("a\n  (b\n  c")
    assert not report
    assert report.line == 2
    assert report.column == 3
    assert report.character == "("
    assert "non fermée" in report.message


def test_report_truthiness():
    assert BracketReport(True)
    assert not BracketReport(False, 1, 1, "(", "non fermée")


def test_analyse_file(tmp_path):
    valid = tmp_path / "valid.html"
    valid.write_text("<html><body>[ok]</body></html>", encoding="utf-8")
    assert analyse_file(valid).valid

    invalid = tmp_path / "invalid.html"
    invalid.write_text("<html>\n  <body>(</body>\n</html>", encoding="utf-8")
    report = analyse_file(invalid)
    assert not report
    assert report.line == 2
    assert report.character == "("
