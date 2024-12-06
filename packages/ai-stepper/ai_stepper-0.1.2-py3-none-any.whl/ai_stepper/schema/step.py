from pydantic import BaseModel
from typing import Dict, Any, Optional, Union

class InputDefinition(BaseModel):
    type: str
    items: Optional[Dict[str, Any]] = None

class Step(BaseModel):
    task: str
    inputs: Dict[str, Union[str, InputDefinition]]
    outputs: Dict[str, Any]
    max_retries: Optional[int] = 3