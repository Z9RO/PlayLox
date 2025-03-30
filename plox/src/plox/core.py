from sys import stdin
from plox.error import reset
from plox.scanner import Scanner

def _run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(token)

def _run_file(source_file: str) -> None:
    with open(source_file, "r") as f:
        content = f.read()
        _run(content)


def _run_prompt() -> None:
    for line in stdin:
        reset()
        _run(line)



def main(args: list[str] | None = None) -> None:
    if (args is None) or len(args) == 0:
        _run_prompt()
    elif len(args) == 1:
        _run_file(args[0])
    else:
        print("Usage: plox [script]")
        exit(64)
