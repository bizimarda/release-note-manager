from agents.agents import BaseAgent

class ProjectPlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ProjectPlanningAgent",
            description="Plans project structure and milestones"
        )
    
    def execute(self, input_data: Dict[str, str]) -> Dict[str, str]:
        project_goal = input_data.get("goal", "")
        
        plan = {
            "phases": ["Planning", "Development", "Testing", "Deployment"],
            "timeline": "Estimated: 4-6 weeks",
            "milestones": []
        }
        
        return {"project_plan": plan}