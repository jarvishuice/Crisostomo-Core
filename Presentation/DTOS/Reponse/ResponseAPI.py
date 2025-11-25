from typing import Optional, Any
from pydantic import BaseModel

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[Any] = None
