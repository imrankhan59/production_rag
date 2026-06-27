from hashlib import sha256
from pathlib import Path


class HashingService:
    """
    Responsible only for generating SHA-256 hashes.

    This service does not:
    - access the database
    - extract metadata
    - interact with RabbitMQ
    - contain business logic
    """

    CHUNK_SIZE = 1024 * 1024  # 1 MB

    @classmethod
    def calculate_sha256(cls, file_path: Path) -> str:
        """
        Calculate the SHA-256 hash of a file.

        Args:
            file_path: Path to the file.

        Returns:
            Hexadecimal SHA-256 hash string.

        Raises:
            FileNotFoundError:
                If the file does not exist.

            IsADirectoryError:
                If the provided path is a directory.
        """

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.is_file():
            raise IsADirectoryError(f"Expected a file but got: {file_path}")

        hasher = sha256()

        with file_path.open("rb") as file:
            while chunk := file.read(cls.CHUNK_SIZE):
                hasher.update(chunk)

        return hasher.hexdigest()