from typing import Dict, Any
from .generator import GeneratorAgent
from .reviewer import ReviewerAgent

class Pipeline:
    def __init__(self):
        self.generator = GeneratorAgent()
        self.reviewer = ReviewerAgent()

    def run(self, grade: int, topic: str) -> Dict[str, Any]:
        """
        Executes the generation pipeline:
        1. Generate content
        2. Review content
        3. Simple refinement loop (max 1 pass) if review fails
        """
        
        # Step 1: Initial Generation
        print(f"Generating content for Grade {grade}, Topic: {topic}...")
        initial_output = self.generator.generate(grade, topic)
        
        # Step 2: Review
        print("Reviewing content...")
        review_output = self.reviewer.review(initial_output, grade, topic)
        
        refined_output = None
        
        # Step 3: Refinement (if valid fail)
        if review_output["status"] == "fail":
            print("Review failed. Refining content...")
            feedback = review_output.get("feedback", [])
            refined_output = self.generator.generate(grade, topic, feedback=feedback)
            # Re-review is not required by spec ("One refinement pass is allowed"), 
            # and output schema just asks for refined output.
        
        return {
            "initial_output": initial_output,
            "review_output": review_output,
            "refined_output": refined_output
        }
