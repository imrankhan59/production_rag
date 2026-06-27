from pathlib import Path

from rag_project.scanner.folder_watcher import FolderWatcher


watcher = FolderWatcher(
    Path("data/raw")
)

watcher.start()