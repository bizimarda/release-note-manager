from agents.agents import BaseAgent

class TechnologySelectionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TechnologySelectionAgent",
            description="Recommends appropriate technologies for projects"
        )
    
    def execute(self, input_data: Dict[str, str]) -> Dict[str, str]:
        project_type = input_data.get("project_type", "web")
        requirements = input_data.get("requirements", "")
        
        tech_stack = {
            "language": "Python",
            "framework": "FastAPI" if project_type == "api" else "React",
            "database": "PostgreSQL",
            "deployment": "Docker"
        }
        
        return {"tech_stack": tech_stack}