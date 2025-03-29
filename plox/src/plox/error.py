import sys


__has_error = False


def has_error() -> bool:
    return __has_error


def reset() -> None:
    __has_error = False


def error(line: int, message: str) -> None:
    __report(line, "", message)


def __report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    __has_error = True
