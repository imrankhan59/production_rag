from pathlib import Path

from rag_project.observability.config import configure_logging
from rag_project.scanner.initial_scanner import InitialScanner


def main() -> None:
    configure_logging()

    directory = Path("data/raw")

    scanner = InitialScanner(directory)
    scanner.scan()


if __name__ == "__main__":
    main()