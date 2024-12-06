from typing import Dict
from pydantic import BaseModel

class UploadUrls(BaseModel):
    presigned_urls: Dict[str, str]
    job_id: str
