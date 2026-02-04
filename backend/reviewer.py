import os
import json
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

class ReviewerAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def review(self, content: Dict[str, Any], grade: int, topic: str) -> Dict[str, Any]:
        """
        Reviews the generated content for quality and correctness.
        """
        
        system_instruction = """
        You are an educational content reviewer.
        Evaluate the provided content based on:
        1. Age appropriateness (is the language suitable for the target grade?)
        2. Conceptual correctness (are facts accurate?)
        3. Clarity (is the explanation and questions easy to understand?)
        
        Input is a JSON object with "explanation" and "mcqs".
        
        STRICT JSON OUTPUT REQUIRED:
        {
          "status": "pass" | "fail",
          "feedback": [
            "<string>"
          ]
        }
        
        If status is "fail", provide specific, actionable feedback strings in the list.
        If status is "pass", feedback list can be empty or contain positive remarks.
        """

        prompt = f"""
        Target Grade: {grade}
        Target Topic: {topic}
        
        Content to Review:
        {json.dumps(content)}
        """

        full_prompt = f"{system_instruction}\n\n{prompt}"

        try:
            response = self.model.generate_content(
                contents=full_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error in ReviewerAgent: {e}")
            return {
                "status": "fail",
                "feedback": [f"Review process failed due to error: {str(e)}"]
            }

if __name__ == "__main__":
    # Test
    try:
        agent = ReviewerAgent()
        sample_content = {
            "explanation": "Photosynthesis is how plants eat.",
            "mcqs": []
        }
        print(agent.review(sample_content, 5, "Photosynthesis"))
    except Exception as e:
        print(e)
