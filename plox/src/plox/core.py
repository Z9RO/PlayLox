def runFile(source: str) -> None:
    print(f"run source file {source}")

def runPrompt()-> None:
    print("run prompt")

def main(args: list[str] | None = None) -> None:
    if (args is None) or len(args) == 0:
        runPrompt()
    elif len(args) == 1:
        runFile(args[0])
    else:
        print("Usage: plox [script]")
        exit(64)
