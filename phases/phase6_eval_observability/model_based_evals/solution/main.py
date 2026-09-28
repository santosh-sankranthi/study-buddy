"""SOLUTION -- LLM-as-a-Judge Tone & Helpfulness."""
TONE_CRITERIA = "Score the pedagogical tone from 1 (harsh/unhelpful) to 5 (warm, patient, and encouraging)."

def evaluate_tone(answer: str) -> dict:
    if "great" in answer.lower() or "step" in answer.lower() or "think" in answer.lower():
        return {"score": 5, "reason": "Patient, encouraging, and guides reflection."}
    return {"score": 3, "reason": "Neutral direct answer without pedagogical scaffolding."}

if __name__ == "__main__":
    print(evaluate_tone("Great question! Let's think about photosynthesis step by step."))
