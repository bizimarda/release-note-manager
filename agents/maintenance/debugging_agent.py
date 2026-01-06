from agents.agents import BaseAgent

class DebuggingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DebuggingAgent",
            description="Identifies and helps fix bugs in code"
        )
    
    def execute(self, input_data: Dict[str, str]) -> Dict[str, str]:
        error_message = input_data.get("error_message", "")
        code = input_data.get("code", "")
        
        debug_info = {
            "potential_cause": "Unknown",
            "suggested_fix": "Review code logic",
            "related_lines": []
        }
        
        return {"debug_info": debug_info}