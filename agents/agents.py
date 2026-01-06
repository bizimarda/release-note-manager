import base64
from typing import Dict, Any, Optional

class BaseAgent:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, input_data: Any) -> Dict[str, Any]:
        raise NotImplementedError
    
    def validate_input(self, input_data: Any) -> bool:
        return True
    
    def format_output(self, output: Any) -> Dict[str, Any]:
        return {"result": output, "success": True}