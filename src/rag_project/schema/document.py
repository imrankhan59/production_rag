from datetime import datetime
from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    file_name: str
    file_path: str
    file_extension: str
    file_size: int
    sha256_hash: str
    source_created_at: datetime
    source_modified_at: datetime

