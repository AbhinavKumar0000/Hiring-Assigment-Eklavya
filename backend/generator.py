import os
import json
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

class GeneratorAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate(self, grade: int, topic: str, feedback: List[str] = None) -> Dict[str, Any]:
        """
        Generates educational content based on grade and topic.
        If feedback is provided, it refines the content.
        """
        
        system_instruction = f"""
        You are an educational content generator. 
        Your task is to generate content for a specific grade level and topic.
        
        STRICT JSON OUTPUT REQUIRED.
        Output format:
        {{
          "explanation": "<string>",
          "mcqs": [
            {{
              "question": "<string>",
              "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
              "answer": "<one of A/B/C/D>"
            }}
          ]
        }}
        
        Rules:
        - Generate exactly 3 MCQs.
        - Options must be labeled A, B, C, D.
        - Explanation should be concise but informative (approx 100-150 words).
        - Ensure language is appropriate for Grade {grade}.
        """

        prompt = f"Generate 3 multiple choice questions and an explanation for Grade {grade} students on the topic: '{topic}'."

        if feedback:
            prompt += f"\n\nPlease refine the previous output based on the following feedback:\n"
            for item in feedback:
                prompt += f"- {item}\n"
            prompt += "\nEnsure all issues are addressed in this new version."

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
            print(f"Error in GeneratorAgent: {e}")
            return {
                "explanation": f"Failed to generate content due to error: {str(e)}",
                "mcqs": []
            }

if __name__ == "__main__":
    # Test
    try:
        agent = GeneratorAgent()
        print(agent.generate(5, "Photosynthesis"))
    except Exception as e:
        print(e)
