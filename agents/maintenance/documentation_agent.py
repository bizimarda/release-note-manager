from agents.agents import BaseAgent

class DocumentationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DocumentationAgent",
            description="Generates documentation for code and projects"
        )
    
    def execute(self, input_data: Dict[str, str]) -> Dict[str, str]:
        code = input_data.get("code", "")
        doc_type = input_data.get("type", "readme")
        
        documentation = f"# Documentation\n\nGenerated based on code analysis.\n"
        
        return {"documentation": documentation, "type": doc_type}