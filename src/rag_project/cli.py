from rag_project.config import get_settings


def main() -> None:
    settings = get_settings()
    print(f"RAG project ready. Data dir: {settings.data_dir}")


if __name__ == "__main__":
    main()
