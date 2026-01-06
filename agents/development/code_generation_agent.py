from agents.agents import BaseAgent

class CodeGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CodeGenerationAgent",
            description="Generates code based on requirements"
        )
    
    def execute(self, input_data: Dict[str, str]) -> Dict[str, str]:
        requirements = input_data.get("requirements", "")
        language = input_data.get("language", "python")
        
        generated_code = f"# Generated {language} code for: {requirements}\n"
        generated_code += f"# TODO: Implement {requirements}\n"
        
        return {"code": generated_code, "language": language}