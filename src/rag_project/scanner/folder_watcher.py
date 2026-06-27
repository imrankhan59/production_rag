from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from rag_project.workers.publisher import TaskPublisher


class DocumentEventHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self._publisher = TaskPublisher()

    def on_created(self, event) -> None:
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix.lower() != ".pdf":
            return

        self._publisher.publish_document(file_path)


class FolderWatcher:
    def __init__(self, directory: Path) -> None:
        self._directory = directory
        self._observer = Observer()

    def start(self) -> None:
        event_handler = DocumentEventHandler()

        self._observer.schedule(
            event_handler,
            str(self._directory),
            recursive=False,
        )

        self._observer.start()

        try:
            self._observer.join()
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        self._observer.stop()
        self._observer.join()