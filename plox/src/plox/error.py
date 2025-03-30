import sys


_has_error = False


def has_error() -> bool:
    return _has_error


def reset() -> None:
    global _has_error
    _has_error = False


def error(line: int, message: str) -> None:
    _report(line, "", message)


def _report(line: int, where: str, message: str) -> None:
    global _has_error
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    _has_error = True
