from agents.agents import BaseAgent

class CodeReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CodeReviewAgent",
            description="Reviews code for quality and best practices"
        )
    
    def execute(self, input_data: Dict[str, str]) -> Dict[str, str]:
        code = input_data.get("code", "")
        
        review = {
            "issues": [],
            "suggestions": [],
            "overall_score": "N/A"
        }
        
        if not code.strip():
            review["issues"].append("Empty code provided")
        
        return {"review": review, "analyzed_code": code[:100]}