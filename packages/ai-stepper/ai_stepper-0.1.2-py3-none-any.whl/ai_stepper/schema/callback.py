from typing import Optional, Callable
from pydantic import BaseModel
from datetime import datetime

class TokensItem(BaseModel):
    """Token usage information for a completion."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class CodeItem(BaseModel):
    """Code item in a callback."""
    content: str
    language: str = "python"

class CallBack(BaseModel):
    """Callback data structure."""
    sender: str
    step_name: Optional[str] = None
    object: str
    message: str
    code: Optional[CodeItem] = None
    tokens: Optional[TokensItem] = None
    created: int = int(datetime.now().timestamp())

# Define callback function type
CallbackFn = Callable[[CallBack], None]

def DEFAULT_CALLBACK(callback_data: CallBack) -> None:
    """Default callback function that does nothing."""
    pass