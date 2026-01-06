from agents.agents import BaseAgent

class ArchitectureAdvisorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ArchitectureAdvisorAgent",
            description="Provides architectural guidance for projects"
        )
    
    def execute(self, input_data: Dict[str, str]) -> Dict[str, str]:
        requirements = input_data.get("requirements", "")
        scale = input_data.get("scale", "small")
        
        recommendations = {
            "pattern": "MVC" if scale == "small" else "Microservices",
            "database": "SQLite" if scale == "small" else "PostgreSQL",
            "framework": "Flask" if scale == "small" else "FastAPI"
        }
        
        return {"recommendations": recommendations}